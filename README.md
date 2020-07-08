# HYBRID-REST-TOPIC
Here we provide a similarity-based search engine based on approximate k-NN search over document embeddings. k-NN ability and indexing documents along with their vector reprsentation is provided by [**OpenDistro for ElasticSearch**](https://opendistro.github.io/for-elasticsearch/) and document embedding is extrapolated from individual words embeddings obtained from pre-trained and aligned [**FastText**](https://fasttext.cc/docs/en/aligned-vectors.html) dictionaries in french, german, english and italian. 
The process of generating vector representations of documents is handled by a simple REST API built with the [**Django REST framework**](https://www.django-rest-framework.org/)
Typical use-case of our solution : recommendation and suggestion based on a reference document or natural language queries.


# Requirements
Python 3 and the following modules should be installed :
- django
- djangorestframework
- spacy (the 4 language models should also be downloaded)
- numpy
- scikit-learn

Also you should have dictionaries with word embeddings  
We used the aligned pre-trained vectors dictionaries from FastText [1, 2]  
You can found them here : https://fasttext.cc/docs/en/aligned-vectors.html

---

#### References for fastText aligned dictionaries 
<a id="1">[1]</a> 
Joulin, A., Bojanowski, P., Mikolov, T., Jégou, H., & Grave, E. (2018). 
Loss in Translation: Learning Bilingual Word Mapping with a Retrieval Criterion. 
In Proceedings of the 2018 Conference on Empirical Methods in Natural Language Processing.

<a id="2">[2]</a> 
Bojanowski, P., Grave, E., Joulin, A., & Mikolov, T. (2017). 
Enriching Word Vectors with Subword Information.
Transactions of the Association for Computational Linguistics, 5, 135–146.

---

# Installation
## Install python3 (for windows)
<pre>choco install python3 --pre</pre>

## Install modules
On the terminal of PyCharm type the following command:

<pre>
pip install django
pip install djangorestframework
pip install spacy
pip install numpy
pip install scikit-learn
</pre>

## Download the dictionaries
On the terminal of PyCharm type the following command:
<pre>
python3 -m spacy download de_core_news_sm
python3 -m spacy download fr_core_news_sm
python3 -m spacy download en_core_web_sm
python3 -m spacy download it_core_news_sm
</pre>

## Run/Debug configuration in PyCharm
Open the Run/Debug Configurations editor and create a new python configuration:

| Parameter          |      Value                                     |
|--------------------|------------------------------------------------|
| Script path        | ...../HYBRID-REST-TOPIC/vectoREST/manage.py    |
| Parameters         | runserver                                      |
| Python interpreter | Choose the last version of Python3             |
| Working directory  | ...../HYBRID-REST-TOPIC/vectoREST              |


# How to use it ?
...work in progress...
