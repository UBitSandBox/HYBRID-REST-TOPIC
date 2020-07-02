from django.apps import AppConfig
import spacy
import numpy
from sklearn.cluster import KMeans
from sklearn.cluster import AgglomerativeClustering


class Doc2VecConfig(AppConfig):
    name = 'doc2vec'
    en_nlp = spacy.load("en_core_web_sm")
    it_nlp = spacy.load("it_core_news_sm")
    fr_nlp = spacy.load("fr_core_news_sm")
    de_nlp = spacy.load("de_core_news_sm")

    km = KMeans(n_clusters = 3)
    ac = AgglomerativeClustering(n_clusters = 3)

    def vectorise(word, lang):
        ### Random vector generation for testing purpose
        return numpy.random.random(300).tolist()
    
    def aggregate(vectors, method):
        method_switcher = {
            'k-means' : Doc2VecConfig.km.fit_predict,
            'agglomerative' : Doc2VecConfig.ac.fit_predict
        }
        assert method in method_switcher, "invalid method"
        labels = method_switcher[method](vectors).tolist()
        main_cluster = max(set(labels), key=labels.count)
        return numpy.mean([vector for (vector, should_keep) in zip(vectors, [label == main_cluster for label in labels]) if should_keep], axis=0).tolist()
        