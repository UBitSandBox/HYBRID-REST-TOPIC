# HYBRID-TOPIC
Here we provide an Index Manager based on **FAISS** (Facebook Artificial Intelligence Similarity Search) for fast Approximate Nearest-Neighbors search as well as pre-trained and aligned **FastText** dictionaries for word embeddings.
Our IndexManager gives the ability to index text documents (using only the words along with their frequencies for now) as vectors that encapsulate semantic information about its (possibly multiple) topics and quickly search for related documents in this Index that can be stored in a file for easier external access. Typical use : recommendation and suggestion.
# Requirements
Python 3 and the following modules should be installed :
- FAISS
- Spacy
- Numpy
- Scikit-learn

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

# Usage
For now, we use a json for each file as input containing ID as an integer and frequency distribution of words occurences.  
Example :  
{'modelId' : 42, 
 'wordsCount' : {'the' : 2 , 'hitchhiker' : 1 , 'guide' : 1 , 'to' : 1 , 'galaxy' : 1}}
