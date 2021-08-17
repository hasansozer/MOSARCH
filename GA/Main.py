# -*- coding: utf-8 -*-
"""
Created on Wed Aug  4 17:54:58 2021

@author: Milad
"""
import pandas as pd
import numpy as np
from GA import GA
from GAKH import GAKH
from GAJAYA import GAJAYA
import time
import numpy as np
np.random.seed(519)
#%% Input information for Simulation

'''GA-related'''
MaxIts = [10000]                                #Number of iterations
nPops = [30]                                  #Number of population
crossProbs = [0.77]                           #Crossover probability
crossRates = [0.5]                             #Crossover rate  
muteProbs = [0.8]                             #Mutation probability
muteRates = [0.05]                            #Mutation Rate
elitisimProbs = [0.3]                           #Elite Parents Probability
betas = [0.0008]                              #Rollette wheel ratio


'''Problem-related'''
nClusters = [10]                               #Number of Clusters
nModules = 500


#Esad Burdan bana w_ij ve d_i cekermisin?
#########################################################################################################################
w_ij = [list(np.random.randint(0,2,nModules)) for i in range(nModules)]
d_i = np.zeros(nModules)
for i in range(nModules):
    d_i[i] = 0
    for j in range(nModules):
        d_i[i] += w_ij[i][j]
#########################################################################################################################



# =============================================================================
# name='bash-dependency.rsf'
# dataTable =pd.read_table(name,header=None)
# dataTable[0] = dataTable[0].replace('cotain ','')
# dataTable[0] = dataTable[0].map(lambda x: x.lstrip('depends '))
# new = dataTable[0].str.split(" ", n = 1, expand = True)
# 
# uniqueValues1 = new[0].unique()
# uniqueValues2 = new[1].unique()
# uniques1 = [uniqueValues1[i] for i in range(len(uniqueValues1)) if uniqueValues1[i] not in uniqueValues2]
# uniques2 = [uniqueValues2[i] for i in range(len(uniqueValues2)) if uniqueValues2[i] not in uniqueValues1]
# uniques = uniques1 + uniques2
# nModules = len(uniques)
# w_ij = np.zeros((nModules,nModules))
# for i in range(len(uniques)):
#     for j in range(len(uniques)):
#         for k in range(len(new)):
#             if new[0][k] == uniques[i] and new[1][k] == uniques[j]:
#                 w_ij[i][j] = 1
# 
# 
# =============================================================================

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
                                    q=open("Results.txt", "a")
                                    q.write(str(objectiveGA) + '  ' + str(cpuGA) + '  ' + str(objectiveGAKH) + '  ' + str(cpuGAKH) + '  ' + str(objectiveGAJAYA) + '  ' + str(cpuGAJAYA))
                                    q.write('\n')
                                    q.write('\n')
                                    q.close()  
                                                                
                                                        
                                                    