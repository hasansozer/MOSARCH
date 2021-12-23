# -*- coding: utf-8 -*-
"""
Created on Wed Aug  4 17:54:58 2021

@author: Milad
"""
#import pandas as pd
from GA_Parser_Class import *
import time
import numpy as np
import copy
np.random.seed(519)
#%% Input information for Simulation

'''GA-related'''
MaxIts = [10000]                                #Number of iterations
nPops = [30]                                  #Number of population
crossProbs = [0.35]                           #Crossover probability
crossRates = [0.5]                             #Crossover rate  
muteProbs = [0.7]                             #Mutation probability
muteRates = [0.06]                            #Mutation Rate
elitisimProbs = [0.2]                           #Elite Parents Probability
betas = [0.0005]                              #Rollette wheel ratio


'''Problem-related'''                            #Number of Clusters
#nModules = 500

# =============================================================================
dependencyFile = "bash-dependency.rsf"
clusteringFile = "clustered_bash-dependency.rsf"
# =============================================================================

# =============================================================================
dependencyFile = "archstudio-dependency.rsf"
clusteringFile = "clustered_archstudio-dependency.rsf"
# =============================================================================

# =============================================================================
dependencyFile = "hadoop-dependency.rsf"
clusteringFile = "clustered_hadoop-dependency.rsf"
# =============================================================================


# =============================================================================
dependencyFile = "lucene-4.6.1-deps.rsf"
clusteringFile = "clustered_lucene-4.6.1-deps.rsf"
# =============================================================================

# =============================================================================
dependencyFile = "openjpa-2.4.2-deps.rsf"
clusteringFile = "clustered_openjpa-2.4.2-deps.rsf"
# =============================================================================


parser = RSFParser(clusteringFile)
parser.parse_dependency_input_file(dependencyFile)

w_ij = np.array(parser.dsm).astype(int)
d_i = parser.ID2name
d_ii = copy.deepcopy(parser.name2ID)

nModules = len(w_ij)
d_i = np.zeros(nModules)
for i in range(nModules):
    d_i[i] = 0
    for j in range(nModules):
        d_i[i] += w_ij[i][j]

max_num = 0
with open(clusteringFile, "r") as f:
    for line in f:
        line = line.strip().split(" ")
        cluster = int(line[1])
        if cluster > max_num:
            max_num = cluster

modulesOnClusters = [[] for i in range(max_num+1)]
with open(clusteringFile, "r") as f:
    for line in f:
        line = line.strip().split(" ")
        cluster = int(line[1])
        module = d_ii[line[2]]
        modulesOnClusters[cluster].append(module)


m = 0.5 * np.sum(d_i) + 0.00000001
modularity = 0.0
for l in range(len(modulesOnClusters)):
    for i in modulesOnClusters[l]:
            for j in modulesOnClusters[l]:
                modularity += w_ij[i][j] - d_i[i]*d_i[j]/ (2*m)
    modularity = 1/(2*m) * modularity

print(clusteringFile + " Modularity: ", modularity)