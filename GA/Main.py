# -*- coding: utf-8 -*-
"""
Created on Wed Aug  4 17:54:58 2021

@author: Milad
"""
#import pandas as pd
from HYGARII import HYGARII
from HYGARI import HYGARI
from GA import GA
from GAKH import GAKH
from GA_Parser_Class import *
import time
import numpy as np
import sys
np.random.seed(519)
#%% Input information for Simulation

'''GA-related'''
MaxIts = [100]                                # Number of iterations
MaxDurations = [50]                            # Max duration in seconds. Duration has precedence over iterations: If the duration is reached, the algorithm stops even if the iterations are not finished.


nPops = [70]                                  # Number of population
crossRates = [0.2]                             # Crossover rate  
muteRates = [0.06]                            # Mutation Rate

crossProbs = [0.55]                           # Crossover probability
muteProbs = [0.7]                             # Mutation probability
elitisimProbs = [0.3]                           # Elite Parents Probability
betas = [0.0005]                              # Rollette wheel ratio


'''Problem-related'''
nClusters = [3,5,10,15]                               #Number of Clusters
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

isDirected = "undirected"
numRuns = 10

CodeList = parser.name2ID.keys()
Dependencies = [] # Unnecessary, never used
DependencyMatrix = [parser.dsm]
nDependecies = [parser.dependency_count]
dInArray = [parser.d_in]
dOutArray = [parser.d_out]

outFilePrefix = dependencyFile.split("-")[0]
hygar3flag = False


parser.parse_clustering_input_file(mgmc_clustering_file)
jaya_list = parser.get_jaya_random_list(mgmc_clustering_file)
clustered_items = parser.clustered_items
name2ID = parser.name2ID
nCluster = len(clustered_items)
outFileSuffix = str(nCluster) + "clusters" + "-" + isDirected + "-" + str(numRuns) + "runs"
                                        
'''
1- For specific cluster number taken from MGMC clustering file, run GA, GAKH, HYGARI, and HYGARII, 10 times each and save the results & averages in a file .
2- For 3-15 clusters, run GA, GAKH, and HYGARI
'''



q = open(outFilePrefix + "-" + outFileSuffix + "-GA.csv", "a+")
q.write("RUN #,FINAL MODULARITY,TIME TAKEN\n")    
q.close()

q = open(outFilePrefix + "-" + outFileSuffix + "-GAKH.csv", "a+")
q.write("RUN #,FINAL MODULARITY,TIME TAKEN\n")    
q.close()

q = open(outFilePrefix + "-" + outFileSuffix + "-HYGARI.csv", "a+")
q.write("RUN #,FINAL MODULARITY,TIME TAKEN\n")    
q.close()

q = open(outFilePrefix + "-" + outFileSuffix + "-HYGARII.csv", "a+")
q.write("RUN #,FINAL MODULARITY,TIME TAKEN\n")    
q.close()


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
                                    for runNo in range(numRuns):
                                        inputdata = MaxIt, MaxDuration, nPop, crossNumber, muteNumber, muteRate, elitismProb, beta, nCluster, nModules, w_ij, d_i, crossRate, Dependencies, CodeList, DependencyMatrix, nDependecies, dInArray, dOutArray, isDirected, outFilePrefix + "-" + outFileSuffix 
                                        objectiveGA = 0
                                        cpuGA = 0
                                        objectiveGAKH = 0 
                                        cpuGAKH = 0


                                        start = time.time()
                                        objectiveGA, _ = GA(inputdata)
                                        cpuGA = time.time()-start
                                        with open(outFilePrefix + "-" + outFileSuffix + "-GA.csv", "a+") as q:
                                            q.write(str(runNo) + "," + str(objectiveGA) + "," + str(cpuGA) + '\n')
                                        

                                        start = time.time()
                                        objectiveGAKH, _ = GAKH(inputdata)
                                        cpuGAKH = time.time()-start
                                        with open(outFilePrefix + "-" + outFileSuffix + "-GA.csv", "a+") as q:
                                            q.write(str(runNo) + "," + str(objectiveGAKH) + "," + str(cpuGAKH) + '\n')


                                        start = time.time()
                                        objectiveHYGARI, _ = HYGARI(inputdata)
                                        cpuHYGARI = time.time()-start
                                        with open(outFilePrefix + "-" + outFileSuffix + "-HYGARI.csv", "a+") as q:
                                            q.write(str(runNo) + "," + str(objectiveHYGARI) + "," + str(cpuHYGARI) + '\n')
                                        

                                        start = time.time()
                                        objectiveHYGARII, _ = HYGARII(inputdata, jaya_list, clustered_items, name2ID)
                                        cpuHYGARII = time.time()-start
                                        with open(outFilePrefix + "-" + outFileSuffix + "-HYGARII.csv", "a+") as q:
                                            q.write(str(runNo) + "," + str(objectiveHYGARII) + "," + str(cpuHYGARII) + '\n')
                                    


                                    for nCluster in nClusters:
                                        start = time.time()
                                        objectiveGA, _ = GA(inputdata)
                                        cpuGA = time.time()-start
                                        with open(outFilePrefix + "-" + outFileSuffix + "-GA.csv", "a+") as q:
                                            q.write(str(runNo) + "," + str(objectiveGA) + "," + str(cpuGA) + '\n')
                                        

                                        start = time.time()
                                        objectiveGAKH, _ = GAKH(inputdata)
                                        cpuGAKH = time.time()-start
                                        with open(outFilePrefix + "-" + outFileSuffix + "-GA.csv", "a+") as q:
                                            q.write(str(runNo) + "," + str(objectiveGAKH) + "," + str(cpuGAKH) + '\n')


                                        start = time.time()
                                        objectiveHYGARI, _ = HYGARI(inputdata)
                                        cpuHYGARI = time.time()-start
                                        with open(outFilePrefix + "-" + outFileSuffix + "-HYGARI.csv", "a+") as q:
                                            q.write(str(runNo) + "," + str(objectiveHYGARI) + "," + str(cpuHYGARI) + '\n')
                                        