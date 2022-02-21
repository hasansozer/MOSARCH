# -*- coding: utf-8 -*-
"""
Created on Wed Aug  4 17:54:58 2021

@author: Milad
"""
#import pandas as pd
from GA import GA
from GAKH import GAKH
from GAJAYA import GAJAYA
from GA_Parser_Class import *
import time
import numpy as np
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


'''Problem-related'''
nClusters = [3,5,10,15]                               #Number of Clusters
#nModules = 500

# =============================================================================
dependencyFile = "bash-dependency.rsf"
clusteringFile = "bash-clustering.rsf"
nClusters = [3]
# =============================================================================

# =============================================================================
#dependencyFile = "archstudio-dependency.rsf"
#clusteringFile = "archstudio-clustering.rsf"
#nClusters = [3]
# =============================================================================

# =============================================================================
#dependencyFile = "hadoop-dependency.rsf"
#clusteringFile = "hadoop-clustering.rsf"
#nClusters = [3]
# =============================================================================



parser = RSFParser(clusteringFile)
parser.parse_dependency_input_file(dependencyFile)

w_ij = np.array(parser.dsm).astype(int)
d_i = parser.ID2name

nModules = len(w_ij)
d_i = np.zeros(nModules)
for i in range(nModules):
    d_i[i] = 0
    for j in range(nModules):
        d_i[i] += w_ij[i][j]


q1 = open("Results.csv", "w+")
q1.write("")
q1.close()

#%% Main Loop
for MaxIt in MaxIts:
    for nPop in nPops:
        for crossProb in crossProbs:
            crossNumber = 2*int(crossProb*nPop/2)
            for crossRate in crossRates:
                for muteProb in muteProbs:
                    muteNumber=int(muteProb*nPop)
                    for muteRate in muteRates:
                        for elitismProb in elitisimProbs:
                            for beta in betas:
                                for nCluster in nClusters:
                                    q=open("Results.csv", "a")
                                    q.write(str(nCluster) + ': ')
                                    q.write('\n')
                                    q.close()
                                    inputdata = MaxIt, nPop, crossNumber, muteNumber, muteRate, elitismProb, beta, nCluster, nModules, w_ij, d_i, crossRate
                                    start = time.time()
                                    objectiveGA, clusters = GA(parser,inputdata)
                                    q=open("Results.csv", "a")
                                    q.write('\n')
                                    q.close()
                                    cpuGA = time.time()-start
                                    start = time.time()
                                    objectiveGAKH, clusters = GAKH(parser,inputdata)
                                    q=open("Results.csv", "a")
                                    q.write('\n')
                                    q.close()                                    
                                    cpuGAKH = time.time()-start
                                    start = time.time()
                                    objectiveGAJAYA, clusters = GAJAYA(parser,inputdata)
                                    cpuGAJAYA = time.time()-start
                                    q=open("Results.csv", "a")
                                    q.write('\n')
                                    q.close()       