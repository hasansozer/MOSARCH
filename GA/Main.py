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
#from GAParser import GAParser
import time
import numpy as np
np.random.seed(519)
#%% Input information for Simulation

def GAParser(dependency, clustering):
	GAParser.dependency = dependency
	GAParser.clustering = clustering
	GAParser.clustered_items = []
	GAParser.name2ID = {}
	GAParser.ID2name = {}
	GAParser.total_item_count = 0
	parse_clustering_input_file(GAParser, GAParser.clustering)
	GAParser.dsm = [[False for x in range(GAParser.total_item_count)] for y in range(GAParser.total_item_count)]
	parse_dependency_input_file(GAParser, GAParser.dependency)
	dsm_np = np.array([elem for row in GAParser.dsm for elem in row])
	
	return(dsm_np,GAParser.ID2name, GAParser.clustered_items)

def dependency(parser,e1,e2):
	sum = 0
	if parser.dsm[parser.name2ID.get(e1)][parser.name2ID.get(e2)]: sum+=1
	if parser.dsm[parser.name2ID.get(e2)][parser.name2ID.get(e1)]: sum+=1
	return sum

def parse_clustering_input_file(parser,filename):
	try:
		f = open(filename, "r+")
		cluster_name = ""
		current_cluster = ""
		item_name = ""
		cluster_count = 0
		
		for line in f:
			tokens = line.split()
			cluster_name = tokens[1]
			if current_cluster != cluster_name:
				current_cluster = cluster_name
				cluster_count += 1
				parser.clustered_items.append([])	 
			

			item_name = tokens[2]
			parser.clustered_items[cluster_count-1].append(item_name)
			parser.ID2name.update({parser.total_item_count: item_name })
			parser.name2ID.update({item_name: parser.total_item_count })
			parser.total_item_count += 1
		f.close()
	except:
		print("Error while reading clustering input file!")

def parse_dependency_input_file(parser, filename):
	try:
		f = open(filename, "r+")
		
		for line in f:
			tokens = line.split()
			item_name = tokens[1]
			parser.dsm[parser.name2ID.get(item_name)][parser.name2ID.get(tokens[2])] = True

		f.close()

	except:
		print("Error while reading the dependency input file!")



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
#nClusters = [10]                               #Number of Clusters
#nModules = 500


#Esad Burdan bana w_ij ve d_i cekermisin?
#########################################################################################################################
w_ij, d_i, clustered_items = GAParser('bash-dependency.rsf', 'bash-clustering.rsf')
#########################################################################################################################
# w_ij : 2D matrix showing the dependencies between files, True or False for each cell in the matrix
# d_i  : index to name map
# clustered_items : list of clusters that contain module names, each cluster is also a list

nModules = len(w_ij)
nClusters = [len(clustered_items)]

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
                                                                
                                                        
                                                    