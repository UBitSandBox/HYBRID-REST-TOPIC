import json2vec
import time
import os

dir_path = os.path.dirname(os.path.realpath(__file__))  # Path where the module was loaded
index_file_name = "my.index"
test_lang = "de"
json_path = "json/de/"

if not os.path.exists(os.path.join(dir_path, index_file_name)):
    start = time.clock()
    IM = json2vec.IndexManager()
    IM.set_dictionary(test_lang)
    mid = time.clock()
    path = os.path.join(dir_path, json_path)
    files = os.listdir(path)
    for file in files:
        IM.add(path + file)
    IM.save(os.path.join(dir_path, index_file_name))
    end = time.clock()
    print("Loading dictionary in", mid - start, "seconds. Adding", IM.size(), "files to the index in", end - mid,
          "seconds")

IM = json2vec.IndexManager(os.path.join(dir_path, index_file_name))

try:
    start = time.clock()
    Distances, IDs = zip(*IM.search(2000, 10))
    end = time.clock()
    print(Distances)
    print(IDs)
    print("Found in", end - start, "seconds.")
except:
    pass


