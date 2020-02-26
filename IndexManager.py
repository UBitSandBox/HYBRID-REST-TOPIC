import faiss
import numpy as np
import json
import os
from sklearn.cluster import AgglomerativeClustering
import spacy


class IndexManager:
    __nlp = None
    __lang = None
    __n_clusters = 5  # number of topics clusters by document
    __cluster_weight_threshold = 1/__n_clusters  # a cluster containing a smaller proportion of words won't be kept
    __cluster_affinity = "cosine"  # Can be “euclidean”, “l1”, “l2”, “manhattan”, “cosine”
    __cluster_linkage = "average"  # Can be “ward” (ONLY FOR EUCLIDEAN), “complete”, “average”, “single”
    """
    ward minimizes the variance of the clusters being merged.
    average uses the average of the distances of each observation of the two sets.
    complete or maximum linkage uses the maximum distances between all observations of the two sets.
    single uses the minimum of the distances between all observations of the two sets.
    """
    __dic_dir = os.path.dirname(os.path.realpath(__file__))  # path of the directory where the dictionaries are
    __json_words_count_label = "wordsCount"  # name of the json field containing our frequency distribution of words
    __json_id_label = "modelId"  # name of the json field storing the document ID
    __fr_dic_name = "wiki.fr.align.vec"  # name of the dictionary file for french
    __en_dic_name = "wiki.en.align.vec"  # name of the dictionary file for english
    __it_dic_name = "wiki.it.align.vec"  # name of the dictionary file for italian
    __de_dic_name = "wiki.de.align.vec"  # name of the dictionary file for german
    __pos_tags_to_keep = ["NN", "NNS", "NNP", "NNPS", "NE", "NNE"]
    __max_clustering_input_size = 1000

    def __init__(self, path=None):
        self.__dim = 300  # size of the vector representation of words
        self.__dic = dict()
        """ Preparing for Hierarchical Clustering with n clusters """
        self.__clusterer = AgglomerativeClustering(n_clusters=self.__n_clusters,
                                                   affinity=self.__cluster_affinity,
                                                   linkage=self.__cluster_linkage)
        if path is None:
            """ If no path is given, we initialise an empty index """
            self.__index = faiss.IndexIDMap2(faiss.IndexFlatL2(self.__dim))
        else:
            """ Otherwise, we load a previously-build index """
            try:
                self.__index = faiss.read_index(path)
            except FileNotFoundError:
                print("Index could not be found or loaded in the path provided.")

    def set_dictionary(self, lang):
        """
        Load the corresponding dictionary in memory
        :param lang: string representing the wanted language
        :return:
        """

        path_switcher = {
            "fr": self.__fr_dic_name,
            "en": self.__en_dic_name,
            "it": self.__it_dic_name,
            "de": self.__de_dic_name
        }

        if lang in path_switcher:
            """ If we have a dictionary for the provided language, we set the path for loading it afterwards """
            dic_path = path_switcher[lang]
        else:
            raise Exception("Language is not recognized, try one of the followings : "
                            +
                            ", ".join([str(key) for key in path_switcher.keys()]))

        dic = {}

        """ Reading the .vec dictionary and storing it in a Python dictionary """
        with open(os.path.join(self.__dic_dir, dic_path), 'r', encoding='utf-8') as f:
            for line in f:
                values = line.rstrip().rsplit(' ')
                word = values[0]
                vector = np.asarray(values[1:], dtype='float32')
                dic[word] = vector

        self.__dic = dic  # Assigning the dictionary to the IndexManager object for out-of-scope usability
        self.__lang = lang
        nlp_loader = {
            "fr": "fr_core_news_sm",
            "de": "de_core_news_sm",
            "en": "en_core_web_sm",
            "it": "it_core_news_sm"
        }
        self.__nlp = spacy.load(nlp_loader[self.__lang], disable=["ner", "parser"])

    def __word2vec(self, word):
        """
        Performs word embedding when possible
        :param word: self-explanatory
        :return: vector representation of the given word, or None if the word is not recognized
        """
        if word in self.__dic:
            """ Recognized words are simply replaced by their vector representation """
            result = self.__dic[word]
        else:
            result = None

        return result

    def __json2vectors_and_weights(self, path):
        """
        Opens a the json at given path and returns vectors and weights
        :param path: self-explanatory
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
        # Here we can aggregate similar lemmas

        """ Replacing words with their vector representation """
        result = []
        for (key, value) in cleaned_content:
            if self.__word2vec(key) is not None:
                result.append((self.__word2vec(key), value))
        if len(result) > self.__max_clustering_input_size:
            result = sorted(result, key=lambda tup: tup[1], reverse=True)[:self.__max_clustering_input_size]
        return result

    def __json2id(self, path):
        """
        Extracts ID from given json
        :param path: path from the json file
        :return: integer representing the "hopefully unique" ID stored in the file
        """
        with open(path, "r", encoding='utf-8') as f:
            int_id = int(json.load(f)[self.__json_id_label])
        return int_id

    def __vectors_grouping(self, vectors):
        """
        :param vectors: list of vectors
        :return: list of integer labels indicating to which cluster the given vectors belong
        by performing Hierarchical Agglomerative Clustering
        """
        self.__clusterer.fit_predict(vectors)
        labels = self.__clusterer.labels_.tolist()
        return labels

    def add(self, path):
        """
        Adding an element
        :param path: path
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

            """ Filtering unsignificant clusters with a threshold """
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
        :param path: path where to save the index
        :return: nothing, saves index in-place
        """
        faiss.write_index(self.__index, path)

    def load(self, path):
        """
        Loads an existing index
        :param path: path
        :return: nothing, loads in-place
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

        distance_list = []
        id_list = []

        ids_to_try = np.arange(self.__n_clusters * document_id, self.__n_clusters * (document_id + 1))
        for id_to_try in ids_to_try:
            try:
                distances, ids = self.__index.search(self.__index.reconstruct(int(id_to_try)).reshape((1, self.__dim)),
                                                     self.__n_clusters * k_neighbors)
                for d in distances:
                    for sub_d in d:
                        distance_list.append(sub_d)
                for i in ids:
                    for sub_i in i:
                        id_list.append(sub_i)
            except:
                pass

        """ Document-level distance is here defined as the minimum of all the distances between topics clusters """
        min_dist = {}

        decreasing_tuples = sorted(list(zip(distance_list, id_list)), key=lambda tup: tup[0], reverse=True)
        for (d, i) in decreasing_tuples:
            min_dist[np.math.floor(i / self.__n_clusters)] = d

        results = sorted(list(min_dist.items()), key=lambda tup: tup[1])[:k_neighbors]
        if len(results) > 0:
            return results
        else:
            raise Exception("Nothing has been found")

    def show(self, document_id):
        """
        Reconstructs the vectors
        :param document_id: ID of the document
        :return: prints reconstructed vectors from document
        """
        vectors = []
        for i in range(self.__n_clusters*document_id, self.__n_clusters*(document_id+1)):
            try:
                vectors.append(self.__index.reconstruct(i))
            except:
                pass
        print(vectors)

    def size(self):
        """
        :return: size of the index
        """
        return self.__index.ntotal
