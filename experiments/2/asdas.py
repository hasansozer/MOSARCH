from GA_Parser_Class import *
import numpy as np


# =============================================================================
# dependencyFile = "bash-dependency.rsf"
# clusteringFile = "clustered_bash-dependency.rsf"
# =============================================================================

# =============================================================================
dependencyFile = "archstudio-dependency.rsf"
clusteringFile = "archstudio-clustering.rsf"
# =============================================================================

# =============================================================================
#dependencyFile = "hadoop-dependency.rsf"
#clusteringFile = "clustered_hadoop-dependency.rsf"
# =============================================================================

# =============================================================================
#dependencyFile = "lucene-4.6.1-deps.rsf"
#clusteringFile = "clustered_lucene-4.6.1-deps.rsf"
# =============================================================================

# =============================================================================
#dependencyFile = "openjpa-2.4.2-deps.rsf"
#clusteringFile = "clustered_openjpa-2.4.2-deps.rsf"
# =============================================================================


parser = RSFParser(clusteringFile)
parser.parse_dependency_input_file(dependencyFile)

w_ij = np.array(parser.dsm).astype(int)
name2id = parser.name2ID
id2name = parser.ID2name

# taken from Milad's code directly
nModules = len(w_ij)
d_i = np.zeros(nModules)
for i in range(nModules):
    d_i[i] = 0
    for j in range(nModules):
        d_i[i] += w_ij[i][j]

max_num = 0

# find how many clusters there are
with open(clusteringFile, "r") as f:
    for line in f:
        line = line.strip().split(" ")
        cluster = int(line[1])
        if cluster > max_num:
            max_num = cluster

# initiate the clusters
modulesOnClusters = [[] for i in range(max_num+1)]


# read the clustering file and put modules on clusters
with open(clusteringFile, "r") as f:
    for line in f:
        line = line.strip().split(" ")
        cluster = int(line[1])
        module = name2id[line[2]]
        modulesOnClusters[cluster].append(module)


m = 0.5 * np.sum(d_i) + 0.00000001
modularity = 0.0
for l in range(len(modulesOnClusters)):
    for i in modulesOnClusters[l]:
            for j in modulesOnClusters[l]:
                modularity += w_ij[i][j] - d_i[i]*d_i[j] / (2*m)
modularity = 1 / (2 * m) * modularity

# for c in range(cluster_count):
#     modules = clustered_items[c]
#     for e1 in range(len(modules)):
#         for e2 in range(e1+1,len(modules)):
#             total += parser.dependency(modules[e1], modules[e2])
#             total -= (d[e1]*d[e2])/(2*m)


print("Modularity: ", modularity)