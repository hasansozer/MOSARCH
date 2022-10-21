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
import sys
np.random.seed(519)
#%% Input information for Simulation

'''GA-related'''
MaxIts = [1]                                # Number of iterations
MaxDurations = [9000]                            # Max duration in seconds. Duration has precedence over iterations: If the duration is reached, the algorithm stops even if the iterations are not finished.


nPops = [70]                                  # Number of population
crossRates = [0.2]                             # Crossover rate  
muteRates = [0.06]                            # Mutation Rate

crossProbs = [0.55]                           # Crossover probability
muteProbs = [0.7]                             # Mutation probability
elitisimProbs = [0.3]                           # Elite Parents Probability
betas = [0.0005]                              # Rollette wheel ratio


'''Problem-related'''
nClusters = [1]                               #Number of Clusters
dependencyFile = sys.argv[1]

parser = RSFParser()
parser.parse_dependency_input_file(dependencyFile)

w_ij = np.array(parser.dsm).astype(int)
d_i = parser.ID2name
clustered_items = parser.clustered_items


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
                                    for nCluster in nClusters:
                                        for metric in ["directed", "undirected"]:

                                            outFileSuffix = str(nCluster) + "clusters-" + metric
                                            inputdata = MaxIt, MaxDuration, nPop, crossNumber, muteNumber, muteRate, elitismProb, beta, nCluster, nModules, w_ij, d_i, crossRate, Dependencies, CodeList, DependencyMatrix, nDependecies, dInArray, dOutArray, metric, outFilePrefix + "-" + outFileSuffix 
                                            objectiveGA = 0
                                            cpuGA = 0
                                            objectiveGAKH = 0 
                                            cpuGAKH = 0
                                            
                                            
                                            q = open(outFilePrefix + "-" + outFileSuffix + "-GA.csv", "w+")
                                            q.write("Iteration,Iteration_CPU_Time,Total_CPU_Time,Objective\n")
                                            q.flush()
                                            q.close()
                                            start = time.time()
                                            objectiveGA, clusters = GA(inputdata)
                                            cpuGA = time.time() - start
                                            q = open(outFilePrefix + "-" + outFileSuffix + "-GA.csv", "a+")
                                            q.write("Final,," + str(cpuGA) + "," + str(objectiveGA) + '\n')
                                            q.flush()
                                            q.close()

                                            
                                            q = open(outFilePrefix + "-" + outFileSuffix + "-GAKH.csv", "w+")
                                            q.write("Iteration,Iteration_CPU_Time,Total_CPU_Time,Objective\n")
                                            q.flush()
                                            q.close()
                                            start = time.time()
                                            objectiveGAKH, clusters = GAKH(inputdata)
                                            cpuGAKH = time.time() - start
                                            q = open(outFilePrefix + "-" + outFileSuffix + "-GAKH.csv", "a+")
                                            q.write("Final,," + str(cpuGA) + "," + str(objectiveGA) + '\n')
                                            q.flush()
                                            q.close()
                                            
                                            
                                            q = open(outFilePrefix + "-" + outFileSuffix + "-GAJAYA.csv", "w+")
                                            q.write("Iteration,Iteration_CPU_Time,Total_CPU_Time,Objective\n")
                                            q.flush()
                                            q.close()
                                            start = time.time()
                                            objectiveGAJAYA, clusters = GAJAYA(inputdata)
                                            cpuGAJAYA = time.time()-start
                                            q = open(outFilePrefix + "-" + outFileSuffix + "-GAJAYA.csv", "a+")
                                            q.write("Final,," + str(cpuGA) + "," + str(objectiveGA) + '\n')
                                            q.flush()
                                            q.close()
