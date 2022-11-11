# -*- coding: utf-8 -*-
"""
Created on Wed Aug  4 17:54:58 2021

@author: Milad
"""
#import pandas as pd
from HYGARIII import HYGARIII
from GA_Parser_Class import *
import time
import numpy as np
import sys
np.random.seed(519)
#%% Input information for Simulation

'''GA-related'''
MaxIts = [100000]                                # Number of iterations
MaxDurations = [9000]                            # Max duration in seconds. Duration has precedence over iterations: If the duration is reached, the algorithm stops even if the iterations are not finished.

nPops = [70]                                  # Number of population
crossRates = [0.2]                             # Crossover rate  
muteRates = [0.06]                            # Mutation Rate

crossProbs = [0.55]                           # Crossover probability
muteProbs = [0.7]                             # Mutation probability
elitisimProbs = [0.3]                           # Elite Parents Probability
betas = [0.0005]                              # Rollette wheel ratio

'''Problem-related'''
dependencyFile = sys.argv[1]
mgmc_clustering_file = sys.argv[1].strip().split("-")[0] + "-clustering.rsf"
print(mgmc_clustering_file)

parser = RSFParser()
parser.parse_dependency_input_file(dependencyFile)

w_ij = np.array(parser.dsm).astype(int)
d_i = parser.ID2name


nModules = len(w_ij)
d_i = np.zeros(nModules)
for i in range(nModules):
    d_i[i] = 0
    for j in range(nModules):
        d_i[i] += w_ij[i][j]

CodeList = parser.name2ID.keys()
Dependencies = [] # Unnecessary, never used
DependencyMatrix = [parser.dsm]
nDependecies = [parser.dependency_count]
dInArray = [parser.d_in]
dOutArray = [parser.d_out]

outFilePrefix = dependencyFile.split("-")[0]

#%% Main Loop
for MaxIt in MaxIts:
    for MaxDuration in MaxDurations:
        for nPop in nPops:
            for crossProb in crossProbs:
                crossNumber = 2*int(crossProb*nPop/2)
                for crossRate in crossRates:
                    for muteProb in muteProbs:
                        muteNumber=int(muteProb*nPop)
                        for muteRate in muteRates:
                            for elitismProb in elitisimProbs:
                                for beta in betas:
                                    parser.parse_clustering_input_file(mgmc_clustering_file)
                                    jaya_list = parser.get_jaya_random_list(mgmc_clustering_file)
                                    clustered_items = parser.clustered_items
                                    name2ID = parser.name2ID
                                    nCluster = len(clustered_items)
                                    outFileSuffix = str(nCluster) + "clusters"
                                    isDirected = False
                                    inputdata = MaxIt, MaxDuration, nPop, crossNumber, muteNumber, muteRate, elitismProb, beta, nCluster, nModules, w_ij, d_i, crossRate, Dependencies, CodeList, DependencyMatrix, nDependecies, dInArray, dOutArray, isDirected, outFilePrefix + "-" + outFileSuffix 
                                    objectiveGA = 0
                                    cpuGA = 0
                                    objectiveGAKH = 0 
                                    cpuGAKH = 0

                                    
                                    q = open(outFilePrefix + "-" + outFileSuffix + "-HYGARIII.csv", "w+")
                                    q.write("Iteration,Iteration_CPU_Time,Total_CPU_Time,Objective\n")
                                    q.flush()
                                    q.close()
                                    start = time.time()

                                    objectiveHYGARIII, clusters = HYGARIII(inputdata, jaya_list, clustered_items, name2ID)
                                    cpuHYGARIII = time.time()-start
                                    q = open(outFilePrefix + "-" + outFileSuffix + "-HYGARIII.csv", "a+")
                                    q.write("Final,," + str(cpuHYGARIII) + "," + str(objectiveHYGARIII) + '\n')
                                    q.flush()
                                    q.close()

