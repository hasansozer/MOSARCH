# -*- coding: utf-8 -*-
"""
Created on Wed Aug  4 17:54:58 2021

@author: Milad
"""
#import pandas as pd
from tblib import Code
from GA import GA
from GAKH import GAKH
from GAJAYA import GAJAYA
from GA_Parser_Class import *
import time
import numpy as np
np.random.seed(519)
#%% Input information for Simulation

'''GA-related'''
MaxIts = [100]                                #Number of iterations


nPops = [70]                                  #Number of population
crossRates = [0.2]                             #Crossover rate  
muteRates = [0.06]                            #Mutation Rate

crossProbs = [0.55]                           #Crossover probability
muteProbs = [0.7]                             #Mutation probability
elitisimProbs = [0.3]                           #Elite Parents Probability
betas = [0.0005]                              #Rollette wheel ratio


'''Problem-related'''
nClusters = [3,5,10,15,20]                               #Number of Clusters
dependencyFile = "bash-dependency.rsf"

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
                                    inputdata = MaxIt, nPop, crossNumber, muteNumber, muteRate, elitismProb, beta, nCluster, nModules, w_ij, d_i, crossRate, Dependencies, CodeList, DependencyMatrix, nDependecies, dInArray, dOutArray
                                    objectiveGA = 0
                                    cpuGA = 0
                                    objectiveGAKH = 0 
                                    cpuGAKH = 0
                                    q=open("Results.csv", "a+")
                                    q.write(str(nCluster) + ': \n')
                                    q.write('GA: \n')
                                    q.close()
                                    start = time.time()
                                    objectiveGA, clusters = GA(inputdata)
                                    cpuGA = time.time()-start
                                    q=open("Results.csv", "a+")
                                    q.write(str(objectiveGA) + ' ' + str(cpuGA) + '\n')	
                                    q.write('GAKH: \n')
                                    q.close()
                                    start = time.time()
                                    objectiveGAKH, clusters = GAKH(inputdata)
                                    cpuGAKH = time.time()-start
                                    q=open("Results.csv", "a+")
                                    q.write(str(objectiveGAKH) + ' ' + str(cpuGAKH) + '\n')
                                    q.write('HYGAR: \n')
                                    q.close()
                                    start = time.time()
                                    objectiveGAJAYA, clusters = GAJAYA(inputdata)
                                    cpuGAJAYA = time.time()-start
                                    q=open("Results.csv", "a+")
                                    q.write(str(objectiveGAJAYA) + ' ' + str(cpuGAJAYA) + '\n')
                                    q.write(str(nPop) + ',' +str(crossProb) + ',' +str(crossRate) + ',' +str(muteProb) + ',' +str(muteRate) + ',' +str(elitismProb) + ',' +str(beta) + ',' +str(objectiveGA) + ',' + str(cpuGA) + ',' + str(objectiveGAKH) + ',' + str(cpuGAKH) + ',' + str(objectiveGAJAYA) + ',' + str(cpuGAJAYA) + '\n')
                                    q.close()
