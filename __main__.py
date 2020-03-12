from IndexManager import IndexManager
import time
import os

dir_path = os.path.dirname(os.path.realpath(__file__))  # Path where the module was loaded
index_relative_path = "saved_indexes/my.index"
test_lang = "de"
json_path = "json_files/de/"

if not os.path.exists(os.path.join(dir_path, index_relative_path)):
    start = time.clock()
    IM = IndexManager(n_clusters=5, cluster_weight_threshold=0.1, max_clustering_input_size=1000,
                      cluster_affinity="euclidean", cluster_linkage="ward", pos_tags_to_keep=["NN"])
    IM.set_parameter("n_clusters", 3)
    IM.set_dictionary(test_lang)
    mid = time.clock()
    path = os.path.join(dir_path, json_path)
    files = os.listdir(path)
    for file in files:
        IM.add(path + file)
    IM.save(os.path.join(dir_path, index_relative_path))
    end = time.clock()
    print("Loading dictionary in", mid - start, "seconds. Adding", IM.get_size(), "files to the index in", end - mid,
          "seconds")

IM = IndexManager(path=os.path.join(dir_path, index_relative_path))
start = time.clock()
Distances, IDs = zip(*IM.search(1000, 10))
end = time.clock()
print(Distances)
print(IDs)
print("Found in", end - start, "seconds.")
