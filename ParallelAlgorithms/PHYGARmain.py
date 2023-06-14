from GA_Parser_Class_New import *
import time
import copy
import numpy as np
from sys import getsizeof
import gc
import subprocess
import os
gc.collect()
import Algorithms

import globals

'''GA-related'''


nPops = [32*6]                                  #Number of population
crossRates = [0.2]                             #Crossover rate  
muteRates = [0.70]                            #Mutation Rate

crossProbs = [0.55]                           #Crossover probability
muteProbs = [0.7]                             #Mutation probability
elitisimProbs = [0.3]                           #Elite Parents Probability
betas = [0.0005]                              #Rollette wheel ratio


globals.tolerance = 1e-6
globals.patience = 50

'''Problem-related'''
nClusters = [5]                               #Number of Clusters


software_list = ["bash"]

algoModes = ["parallel","sequential"]

algorithms = ["GA","HYGAR"]

runInitialHeuristic = True

def runHeuristics(file_name):
    
    instance_name = file_name

    command_1 = "java -jar rsf2txt.jar"

    command_2 = "java -jar clustering.jar"

    command_3 = "java -jar txt2rsf.jar"

    input_1 = "dataset/{}/{}-dependency.rsf".format(instance_name,instance_name)
    output_1 = "dep.txt"

    input_2 = output_1
    output_2 = "c.txt"

    input_3 = output_2
    output_3 = "c.rsf"
    
    
    cmd1 = command_1 + " " + input_1 + " " + output_1
    cmd2 = command_2 + " " + input_2 + " " + output_2
    cmd3 = command_3 + " " + input_3 + " " + output_3
    
    a = subprocess.check_output(cmd1, shell=True,  cwd='experiments/')
    a = subprocess.check_output(cmd2, shell=True,  cwd='experiments/')
    a = subprocess.check_output(cmd3, shell=True,  cwd='experiments/')
    
    target_path = "experiments/" + output_3

    with open(target_path, 'r') as f:
        last_line = f.readlines()[-1]
    n_clust = int(last_line.split(" ")[1]) + 1
    
    return n_clust



if __name__ == "__main__":
    globals.initialize()
    for globals.nPop in nPops:
        for crossProb in crossProbs:
            globals.crossNumber = 2*int(crossProb*globals.nPop/2)
            for globals.crossRate in crossRates:
                for muteProb in muteProbs:
                    globals.muteNumber=int(muteProb*globals.nPop)
                    for globals.muteRate in muteRates:
                        for globals.elitismProb in elitisimProbs:
                            for globals.beta in betas:
                                for globals.nCluster in nClusters:
                                    for globals.software in software_list:
                                        for globals.algoMode in algoModes:
                                            for algorithm in algorithms:

                                                dependencyFile = "dataset/{}/{}-dependency.rsf".format(globals.software,globals.software)

                                                parser = RSFParser(dependencyFile)
                                                parser.parse_dependency_input_file(dependencyFile)

                                                globals.w_ij = np.array(parser.dsm).astype(np.int16)

                                                print("weight matrix sparsity: ",1.0 - (np.count_nonzero(globals.w_ij) / float(globals.w_ij.size)))
                                                print("weight matrix memory usage: ", round(getsizeof(globals.w_ij) / 1024 / 1024,2))

                                                globals.d_i = parser.ID2name
                                                clustered_items = parser.clustered_items
                                                

                                                globals.nModules = len(globals.w_ij)

                                                globals.timeLimit = globals.nModules*5 

                                                globals.d_i = np.zeros(globals.nModules)
                                                for i in range(globals.nModules):
                                                    globals.d_i[i] = 0
                                                    for j in range(globals.nModules):
                                                        globals.d_i[i] += globals.w_ij[i][j]
                                                        
                                                globals.m = 0.5 * np.sum(globals.d_i)                                                    
                                                globals.modMat = np.matmul(globals.d_i.reshape(1,-1).T,globals.d_i.reshape(1,-1))
                                                globals.modMat = globals.modMat/np.sum(globals.d_i)
                                                globals.modMat = globals.modMat.astype(np.float16)

                                                print("modularity matrix sparsity: ",1.0 - (np.count_nonzero(globals.modMat) / float(globals.modMat.size)))
                                                print("modularity graph memory usage: ", round(getsizeof(globals.modMat) / 1024 / 1024,2))

                                                globals.CodeList = list(parser.name2ID.keys())
                                                globals.DependencyMatrix = [parser.dsm]
                                                globals.nDependecies = [parser.dependency_count]
                                                #dInArray = [parser.d_in]
                                                #dOutArray = [parser.d_out]
                                                globals.timeLimit = globals.nModules*5 
                                                print(globals.software, "is being solved", "within time limit of ", globals.timeLimit)
                                                print(globals.software, "has", globals.nModules, "modules")
                                                start = time.time()

                                                if runInitialHeuristic:
                                                    print("Initial clustering algorithm is running....")
                                                    globals.nCluster = runHeuristics(globals.software)
                                                    print("Initial clustering algorithm found {} clusters".format(globals.nCluster))
                                                    globals.logging_directory = globals.logging_directory+ "/Heuristic"
                                                    os.makedirs(globals.logging_directory, exist_ok=True)
                                                    if os.path.exists(globals.logging_directory):
                                                        print(f"Directory '{globals.logging_directory}' created successfully or already exists.")
                                                    else:
                                                        print(f"Failed to create directory '{globals.logging_directory}'.")

                                                if algorithm == "GA":
                                                    objectiveGAJAYA, clusters = Algorithms.GA()
                                                    cpuGAJAYA = time.time()-start
                                                    q=open("{}/Results_{}.csv".format(globals.logging_directory,globals.software), "a+")
                                                    q.write(globals.algoMode +" "+ algorithm +" "+str(objectiveGAJAYA) + ' ' + str(cpuGAJAYA) + '\n')
                                                    q.write(str(globals.nPop) + ',' +str(crossProb) + ',' +str(globals.crossRate) + ',' +str(muteProb) + ',' +str(globals.muteRate) + ',' +str(globals.elitismProb) + ',' +str(globals.beta) + ',' + str(objectiveGAJAYA) + ',' + str(cpuGAJAYA) + '\n')
                                                    q.close()
                                                if algorithm == "HYGAR":
                                                    objectiveGAJAYA, clusters = Algorithms.HYGAR()
                                                    cpuGAJAYA = time.time()-start
                                                    q=open("{}/Results_{}.csv".format(globals.logging_directory,globals.software), "a+")
                                                    q.write(globals.algoMode +" "+ algorithm +" "+ str(objectiveGAJAYA) + ' ' + str(cpuGAJAYA) + '\n')
                                                    q.write(str(globals.nPop) + ',' +str(crossProb) + ',' +str(globals.crossRate) + ',' +str(muteProb) + ',' +str(globals.muteRate) + ',' +str(globals.elitismProb) + ',' +str(globals.beta) + ',' + str(objectiveGAJAYA) + ',' + str(cpuGAJAYA) + '\n')
                                                    q.close()


