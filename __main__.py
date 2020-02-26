import json2vec
import time
import os

dir_path = os.path.dirname(os.path.realpath(__file__))
print(dir_path)

if not os.path.exists(os.path.join(dir_path, "my.index")):
    start = time.clock()
    IM = json2vec.IndexManager()
    IM.set_dictionary('de')
    mid = time.clock()
    path = os.path.join(dir_path, "/json/de/")
    files = os.listdir(path)
    for file in files:
        IM.add(path + file)
    IM.save(os.path.join(dir_path, "my.index"))
    end = time.clock()
    print("Loading dictionary in", mid - start, "seconds. Adding", IM.size(), "files to the index in", end - mid,
          "seconds")

IM = json2vec.IndexManager(os.path.join(dir_path, "my.index"))

try:
    start = time.clock()
    Distances, IDs = zip(*IM.search(2000, 10))
    end = time.clock()
    print(Distances)
    print(IDs)
    print("Found in", end - start, "seconds.")
except:
    pass


