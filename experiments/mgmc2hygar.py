import numpy as np
from numpy import random

if __name__ == '__main__':

    filepath = "C:/Users/hasans/PycharmProjects/ParseClustering/bash-clustering.rsf"

    nModules = 0
    nClusters = 0
    clustered_items = []
    name2ID = {}

    f = open(filepath, "r+")
    cluster_name = ""
    current_cluster = ""
    item_name = ""

    for line in f:
        tokens = line.split()
        cluster_name = tokens[1]
        if current_cluster != cluster_name:
            current_cluster = cluster_name
            nClusters += 1
            clustered_items.append([])

        item_name = tokens[2]
        clustered_items[nClusters - 1].append(item_name)
        name2ID.update({item_name: nModules})
        nModules += 1

    f.close()

    nPop = 10
    population = []

    for p in range(nPop):
        pop_rand = [np.random.random() for _ in range(nModules + nClusters - 1)]
        pop_rand.sort()
        pop = [0.0 for _ in range(nModules + nClusters - 1)]

        cluster_ids = np.arange(0, nClusters).tolist()
        random.shuffle(cluster_ids)

        cluster_start_index = 0
        cluster_stop_index = -1
        while cluster_ids:
            c = cluster_ids.pop()
            cluster_start_index = cluster_stop_index + 1
            cluster_stop_index = cluster_start_index + len(clustered_items[c])
            for i in range(len(clustered_items[c])):
                pop[name2ID[clustered_items[c][i]]] = pop_rand[cluster_start_index + i]
            if len(cluster_ids) > 0:
                pop[nModules+nClusters-len(cluster_ids)-1] = pop_rand[cluster_stop_index]
        population.append(pop)

    print("number of clusters: ", nClusters)
    print("number of modules: ", nModules)

    for p in range(nPop):
        print('population item %d:', p)
        print(population[p])