# HYBRID-TOPIC
Topic modelling, Semantic similarity search  
Here we provide an Index Manager for **FAISS** (Facebook Artificial Intelligence Similarity Search)  
It gives the ability to index text documents (using only the words along with their frequencies for now) as vectors that 
encapsulate semantic information about its (possibly multiple) topics and quickly search for related documents in this Index that can be stored in a file for easier external access. 
# Requirements
Python 3 and the following modules should be installed :
- FAISS
- Spacy
- Numpy
- Scikit-learn

# Usage
For now, we use a json for each file as input containing ID as an integer and frequency distribution of words occurences.  
Example :  
{'modelId' : 42, 
 'wordsCount' : {'the' : 2 , 'hitchhiker' : 1 , 'guide' : 1 , 'to' : 1 , 'galaxy' : 1}}
