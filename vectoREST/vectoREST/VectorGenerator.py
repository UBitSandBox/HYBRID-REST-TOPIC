import spacy
import numpy
from sklearn.cluster import KMeans
from sklearn.cluster import AgglomerativeClustering
from sklearn.cluster import SpectralClustering


class VectorGenerator:
    def __init__(self, method="None", n_clusters=3):
        self.method = method
        self.n_clusters = n_clusters
        assert method in ["None","weighted","k-means","agglomerative","spectral"]
        method_switcher = {
            'k-means' : KMeans,
            'agglomerative' : AgglomerativeClustering,
            'spectral' : SpectralClustering
        }
        if method in ["k-means","agglomerative","spectral"]:
            self.cluster_maker = method_switcher[method](n_clusters=n_clusters)
        self.nlp = spacy.load('xx_use_md')
        self.nlp.add_pipe(self.nlp.create_pipe('sentencizer'))

    def _vectorise_by_sentence(self, document):
        return [self.nlp(str(sent)).vector for sent in self.nlp(document).sents]
    
    def _aggregate(self, vectors):
        if len(vectors) < self.n_clusters:
            mean = numpy.mean(vectors, axis=0)
            weights = [numpy.exp(-numpy.linalg.norm(v-mean)**2) for v in vectors]
            return numpy.average(vectors, axis=0, weights=weights)
        labels = self.cluster_maker.fit_predict(vectors).tolist()
        main_cluster = max(set(labels), key=labels.count)
        return numpy.mean([vector for (vector, should_keep) 
                           in zip(vectors, [label == main_cluster for label in labels]) if should_keep], axis=0).tolist()
    
    def doc2vec(self, document):
        if self.method == "None":
            return self.nlp(document).vector
        elif self.method == "weighted":
            vectors = self._vectorise_by_sentence(document=document)
            mean = numpy.mean(vectors, axis=0)
            weights = [numpy.exp(-numpy.linalg.norm(v-mean)**2) for v in vectors]
            return numpy.average(vectors, axis=0, weights=weights)
        else:
            return self._aggregate(vectors=self._vectorise_by_sentence(document=document))

