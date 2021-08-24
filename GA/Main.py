# -*- coding: utf-8 -*-
"""
Created on Wed Aug  4 17:54:58 2021

@author: Milad
"""
#import pandas as pd
from GA import GA
from GAKH import GAKH
from GAJAYA import GAJAYA
from GA_Parser_Function import RSFParser,parse_dependency_input_file 
from GA_Parser_Class import *
import time
import numpy as np
np.random.seed(519)
#%% Input information for Simulation

'''GA-related'''
MaxIts = [10000]                                #Number of iterations
nPops = [30,50,70]                                  #Number of population
crossProbs = [0.3,0.4,0.5,0.6,0.7]                           #Crossover probability
crossRates = [0.3,0.4,0.5,0.6,0.7]                             #Crossover rate  
muteProbs = [0.6,0.7,0.8,0.9]                             #Mutation probability
muteRates = [0.03,0.04,0.05,0.06]                            #Mutation Rate
elitisimProbs = [0.1,0.2,0.3,0.4]                           #Elite Parents Probability
betas = [0.0005,0.0006,0.0007,0.0008]                              #Rollette wheel ratio


'''Problem-related'''
nClusters = [5]                               #Number of Clusters
#nModules = 500


#Esad Burdan bana w_ij ve d_i cekermisin?
#########################################################################################################################
# =============================================================================
# w_ij = [list(np.random.randint(0,2,nModules)) for i in range(nModules)]
# d_i = np.zeros(nModules)
# for i in range(nModules):
#     d_i[i] = 0
#     for j in range(nModules):
#         d_i[i] += w_ij[i][j]
# =============================================================================
#########################################################################################################################
#w_ij, d_i, clustered_items = GAParser('bash-dependency.rsf', 'bash-clustering.rsf')

dependencyFile = "bash-dependency.rsf";
clusteringFile = "bash-clustering.rsf";

parser = RSFParser(clusteringFile)
parser.parse_dependency_input_file(dependencyFile)


w_ij = np.array(parser.dsm).astype(int)
d_i = parser.ID2name
clustered_items = parser.clustered_items;



nModules = len(w_ij)
d_i = np.zeros(nModules)
for i in range(nModules):
    d_i[i] = 0
    for j in range(nModules):
        d_i[i] += w_ij[i][j]


q1 = open("Results.csv", "w+")
q1.write("nPop,crossProb,crossRate,muteProb,muteRate,elitismProb,beta,objectiveGA,cpuGA,objectiveGAKH,cpuGAKH,objectiveGAJAYA,cpuGAJAYA\n")
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
                                    inputdata = MaxIt, nPop, crossNumber, muteNumber, muteRate, elitismProb, beta, nCluster, nModules, w_ij, d_i, crossRate
                                    start = time.time()
                                    objectiveGA, clusters = GA(inputdata)
                                    cpuGA = time.time()-start
                                    start = time.time()
                                    objectiveGAKH, clusters = GAKH(inputdata)
                                    cpuGAKH = time.time()-start
                                    start = time.time()
                                    objectiveGAJAYA, clusters = GAJAYA(inputdata)
                                    cpuGAJAYA = time.time()-start
                                    q=open("Results.csv", "a")
                                    q.write(str(nPop) + ',' +str(crossProb) + ',' +str(crossRate) + ',' +str(muteProb) + ',' +str(muteRate) + ',' +str(elitismProb) + ',' +str(beta) + ',' +str(objectiveGA) + ',' + str(cpuGA) + ',' + str(objectiveGAKH) + ',' + str(cpuGAKH) + ',' + str(objectiveGAJAYA) + ',' + str(cpuGAJAYA))
                                    q.write('\n')
                                    q.close()  
                                                                
                                                        
                                                    