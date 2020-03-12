import faiss
import numpy as np
import json
import os
from sklearn.cluster import AgglomerativeClustering
import spacy
import itertools


class IndexManager:
    def __init__(self, **kwargs):
        self.__dim = 300
        self.__n_clusters = 5
        self.__cluster_weight_threshold = 0.2
        self.__max_clustering_input_size = 1000
        self.__cluster_affinity = "cosine"
        self.__cluster_linkage = "average"
        self.__dic_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'dictionaries')
        self.__json_words_count_label = "wordsCount"
        self.__json_id_label = "modelId"
        self.__pos_tags_to_keep = ["NN", "NNS", "NNP", "NNPS", "NE", "NNE"]
        self.__alterable_parameters = ["n_clusters", "cluster_weight_threshold", "max_clustering_input_size",
                                       "cluster_affinity", "cluster_linkage", "dic_dir", "json_words_count_label",
                                       "json_id_label", "pos_tags_to_keep"]
        self.__nlp = None
        self.__lang = None
        self.__dic = dict()
        self.__specific_terminology = dict()
        self.__cluster_maker = AgglomerativeClustering(n_clusters=self.__n_clusters,
                                                       affinity=self.__cluster_affinity,
                                                       linkage=self.__cluster_linkage)
        path = kwargs.get('path', None)

        for (k, v) in kwargs.items():
            if hasattr(self, k) and k in self.__alterable_parameters:
                setattr(self, '__' + k, v)

        if path is not None:
            self.__index = faiss.read_index(path)
        else:
            self.__index = faiss.IndexIDMap2(faiss.IndexFlatL2(self.__dim))

    def set_parameter(self, name, value):
        if name in self.__alterable_parameters:
            setattr(self, '__' + name, value)
        else:
            print("No alterable parameter named {}. Try : {}".format(name, ", ".join(self.__alterable_parameters)))

    def set_dictionary(self, lang):
        """
        Load the corresponding dictionary in memory
        :param lang: string representing the wanted language
        :return:
        """
        self.__lang = lang
        self.__nlp = spacy.load("{}_core_{}_sm".format(lang, ("web" if lang == "en" else "news")),
                                disable=["ner", "parser"])

        dic_path = "wiki.{}.align.vec".format(lang)
        dic = {}
        """ Reading the .vec dictionary and storing it in a Python dictionary """
        with open(os.path.join(self.__dic_dir, dic_path), 'r', encoding='utf-8') as f:
            for line in f:
                values = line.rstrip().rsplit(' ')
                word = values[0]
                vector = np.asarray(values[1:], dtype='float32')
                dic[word] = vector
        self.__dic = dic

        specific_path = "{}.term.json".format(lang)
        specific = {}
        try:
            with open(os.path.join(self.__dic_dir, specific_path), 'r', encoding='utf-8') as f:
                specific = json.load(f.read())
        except FileNotFoundError:
            pass
        self.__specific_terminology = specific

    def get_size(self):
        """
        :return: size of the index
        """
        return self.__index.ntotal

    def __word2vec(self, word):
        """
        Performs word embedding when possible
        :param word: string, self-explanatory
        :return: vector representation of the given word, or None if the word is not recognized
        """
        if word in self.__dic:
            """ Recognized words are simply replaced by their vector representation """
            result = self.__dic[word]
        elif word in self.__specific_terminology:
            result = self.__specific_terminology[word]
        else:
            result = None
        return result

    def __json2vectors_and_weights(self, path):
        """
        Opens a .json file at given path and returns vectors and weights
        :param path: string, self-explanatory
        :return: list of tuples [(first_vector, first_weight), ... ]
        """
        with open(path, "r", encoding='utf-8') as f:  # Loads the json file as a dictionary
            words_count = json.load(f)[self.__json_words_count_label]
        content = list(words_count.items())  # Converting it into list of tuples

        """ Pre-processing """
        cleaned_content = []
        words, weights = zip(*content)
        words = list(words)
        weights = list(weights)
        words_to_keep = []
        lemmatizer = {}
        doc = self.__nlp(" ".join(words))
        for token in doc:
            if token.tag_ in self.__pos_tags_to_keep:
                words_to_keep.append(token.text)
                lemmatizer[token.text] = token.lemma_
        for (i, word) in enumerate(words):
            if word in words_to_keep:
                cleaned_content.append((lemmatizer[word], weights[i]))

        """ Here we aggregate possibly similar lemmas """
        dict_holder = {}
        for k, v in cleaned_content:
            if k not in dict_holder:
                dict_holder[k] = v
            else:
                dict_holder[k] += v
        cleaned_content = [(k, v) for k, v in dict_holder.items()]

        """ Replacing words with their vector representation """
        result = []
        for (key, value) in cleaned_content:
            if self.__word2vec(key) is not None:
                result.append((self.__word2vec(key), value))

        """ Truncate result if too many vectors (to have reasonable computing time) """
        if len(result) > self.__max_clustering_input_size:
            result = sorted(result, key=lambda tup: tup[1], reverse=True)[:self.__max_clustering_input_size]
        return result

    def __json2id(self, path):
        """
        Extracts ID from given json
        :param path: string, self-explanatory
        :return: integer representing the "hopefully unique" ID stored in the file
        (FAISS index allows ID duplicates but it will lead to problems when searching for that ID
        so I recommend that you make sure of ID uniqueness before trying to add them to index)
        """
        with open(path, "r", encoding='utf-8') as f:
            int_id = int(json.load(f)[self.__json_id_label])
        return int_id

    def __vectors_grouping(self, vectors):
        """
        :param vectors: list of vectors
        :return: list of integer labels indicating to which cluster the given vectors belongs
        by performing Hierarchical Agglomerative Clustering
        """
        self.__cluster_maker.fit_predict(vectors)
        labels = self.__cluster_maker.labels_.tolist()
        return labels

    def add(self, path):
        """
        Adding an element to the FAISS Index
        :param path: string, path to the json
        :return: boolean answering to "Has the element been successfully added ?"
        If the element is not enough informative for forming topics clusters, it won't be added for example
        """

        try:
            vectors, weights = zip(*self.__json2vectors_and_weights(path))
            labels = self.__vectors_grouping(vectors)
        except:
            labels = None

        if labels is not None:
            """ At this point, we have vectors weights and labels so we can add the document into the index """
            means = []
            cluster_importance = []

            for i in range(self.__n_clusters):
                v, w = zip(*[(vectors[ind], weights[ind]) for (ind, j) in enumerate(labels) if j == i])
                means.append(np.average(v, axis=0, weights=w))
                cluster_importance.append(sum(w))

            """ Filtering un-significant clusters with the threshold we set earlier """
            keep = [c / sum(cluster_importance) > self.__cluster_weight_threshold for c in cluster_importance]

            int_id = self.__json2id(path)
            ids = np.arange(self.__n_clusters * int_id, self.__n_clusters * int_id + sum(keep))

            """ Adding the ones we keep """
            self.__index.add_with_ids(
                np.asarray([m for (i, m) in enumerate(means) if keep[i]], dtype='float32').reshape(sum(keep),
                                                                                                   self.__dim), ids)
            return True
        return False

    def save(self, path):
        """
        Saves current state of the index in a file
        :param path: string, path indicating where to save the index
        """
        faiss.write_index(self.__index, path)

    def load(self, path):
        """
        Loads an existing index
        :param path: path
        """
        try:
            self.__index = faiss.read_index(path)
        except:
            print("No loadable index found.")

    def search(self, document_id, k_neighbors):
        """
        Search for the k documents closest from the one given in input
        :param document_id: ID from the input document
        :param k_neighbors: number of neighbors wanted
        :return: list of IDs and distances of the k nearest neighbors
        """

        ids_to_try = np.arange(self.__n_clusters * document_id, self.__n_clusters * (document_id + 1))

        distance_list = []
        id_list = []
        for id_to_try in ids_to_try:
            try:
                distances, ids = self.__index.search(self.__index.reconstruct(int(id_to_try)).reshape((1, self.__dim)),
                                                     self.__n_clusters * k_neighbors)
                distance_list.extend(itertools.chain(*distances))
                id_list.extend(itertools.chain(*ids))
            except:
                pass

        """ 
        Document-level distance is here defined (for now) as 
        the minimum of all the distances between topics clusters bary-centers 
        """
        min_dist = {}
        decreasing_tuples = sorted(list(zip(distance_list, id_list)), key=lambda tup: tup[0], reverse=True)
        for (d, i) in decreasing_tuples:
            min_dist[np.math.floor(i / self.__n_clusters)] = d

        results = sorted(list(min_dist.items()), key=lambda tup: tup[1])[:k_neighbors]
        if len(results) > 0:
            return results
        else:
            return [(False, False)]

    def show(self, document_id):
        """
        Reconstructs the vectors from ID and print them
        :param document_id: ID of the document
        :return: prints reconstructed vectors associated with the document
        """
        vectors = []
        for i in range(self.__n_clusters * document_id, self.__n_clusters * (document_id + 1)):
            try:
                vectors.append(self.__index.reconstruct(i))
            except:
                pass
        print(vectors)
