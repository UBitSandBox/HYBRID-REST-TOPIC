# HYBRID-REST-TOPIC
Here we provide a similarity-based search engine based on approximate k-NN search over document embeddings. k-NN ability and indexing documents along with their vector reprsentation is provided by [**OpenDistro for ElasticSearch**](https://opendistro.github.io/for-elasticsearch/) and document embedding is using the [**Universal Sentence Encoder - multilingual**](https://tfhub.dev/google/universal-sentence-encoder-multilingual/3) model. 
The process of generating vector representations of documents is handled by a simple REST API built with the [**Django REST framework**](https://www.django-rest-framework.org/)  
Typical use-case of our solution : recommendation and suggestion based on a reference document or natural language queries.


# Requirements
Python 3.x and the following modules should be installed :
- django
- djangorestframework
- spacy
  - *xx_use_md* from [spacy-universal-sentence-encoder-tfhub](https://spacy.io/universe/project/spacy-universal-sentence-encoder)  
`pip install https://github.com/MartinoMensio/spacy-universal-sentence-encoder-tfhub/releases/download/xx_use_md-0.2.3/xx_use_md-0.2.3.tar.gz#xx_use_md-0.2.3`
- numpy
- scikit-learn

---

# Installation

## Install required modules
On a Terminal type the following command:

<pre>
pip install django
pip install djangorestframework
pip install spacy
pip install https://github.com/MartinoMensio/spacy-universal-sentence-encoder-tfhub/releases/download/xx_use_md-0.2.3/xx_use_md-0.2.3.tar.gz#xx_use_md-0.2.3
pip install numpy
pip install scikit-learn
</pre>

## Run/Debug configuration (example in PyCharm)

### In Terminal : 
<pre>
python3 /vectoREST/manage.py runserver
</pre>

### In PyCharm's "Run/Debug Configurations" :

Create a new Python configuration according to the following

| Parameter          |      Value                                     |
|--------------------|------------------------------------------------|
| Script path        | ...../HYBRID-REST-TOPIC/vectoREST/manage.py    |
| Parameters         | runserver                                      |
| Python interpreter | Choose the last version of Python3             |
| Working directory  | ...../HYBRID-REST-TOPIC/vectoREST              |


# How to use it ?
https://documenter.getpostman.com/view/5913280/T17JAnWN
