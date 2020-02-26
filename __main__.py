import json2vec
import time
import os


if not os.path.exists("/home/ubit-mse/PycharmProjects/json2vec/json2vec/my.index"):
    start = time.clock()
    IM = json2vec.IndexManager()
    IM.set_dictionary('de')
    mid = time.clock()
    path = "/home/ubit-mse/PycharmProjects/json2vec/json2vec/json/de/"
    files = os.listdir(path)
    for file in files:
        IM.add(path + file)
    IM.save("/home/ubit-mse/PycharmProjects/json2vec/json2vec/my.index")
    end = time.clock()
    print("Loading dictionary in", mid - start, "seconds. Adding", IM.size(), "files to the index in", end - mid,
          "seconds")

IM = json2vec.IndexManager("/home/ubit-mse/PycharmProjects/json2vec/json2vec/my.index")

try:
    start = time.clock()
    Distances, IDs = zip(*IM.search(2000, 10))
    end = time.clock()
    print(Distances)
    print(IDs)
    print("Found in", end - start, "seconds.")
except:
    pass


