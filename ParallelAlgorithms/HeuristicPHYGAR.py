#from GAJAYA import GAJAYA
from GA_Parser_Class_New import *
import time
import numpy as np
from multiprocessing import Pool
import multiprocessing as mp
import copy
import os
from tqdm import tqdm
import math 
import pandas as pd
import numpy as np
from docplex.mp.model import Model
from docplex.mp.solution import SolveSolution
import cplex
import sys
import pickle
import itertools
from sys import getsizeof
import gc
gc.collect()
import subprocess

print(os.getcwd())

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



np.random.seed(int.from_bytes(os.urandom(4), byteorder='little'))

global  MaxIt, nPop, crossNumber, muteNumber, muteRate, \
        elitismProb, beta, nCluster, nModules, w_ij, d_i, crossRate, \
        Dependencies, CodeList, DependencyMatrix, nDependecies,\
        Probabilities, algoMode, software, modMat, m, timeLimit

'''GA-related'''
MaxIts = [1000]   

                 #Number of iterations


nPops = [32*8]                                  #Number of population
crossRates = [0.2]                             #Crossover rate  
muteRates = [0.70]                            #Mutation Rate

crossProbs = [0.55]                           #Crossover probability
muteProbs = [0.7]                             #Mutation probability
elitisimProbs = [0.3]                           #Elite Parents Probability
betas = [0.0005]                              #Rollette wheel ratio


tolerance = 1e-6
patience = 50
'''Problem-related'''
                              #Number of Clusters
#software_list = ["archstudio","bash","camel","chromium","cxf","hadoop","itk","lucene","nutch","openjpa","struts2","wicket"]

#software_list = ["camel","chromium","cxf","itk"]

software_list = ["bash"]

algoModes = ["parallel","sequential"]

algorithms = ["GA","HYGAR"]


#%% Modularity


##########################################



def SparseGRAPH(clst_cnfg):
    
    myG = np.zeros((nModules,nModules)).astype(np.int16)
    ind = []
    
    for cl in clst_cnfg:
        ind.append(list(itertools.product(cl,cl)))
        
    ind = list(itertools.chain(ind))
    
    for i in ind:
        for i_ in i:
            myG[i_] = 1
    
    np.fill_diagonal(myG, 0)
    #print("sparse graph memory usage: ", round(getsizeof(myG) / 1024 / 1024,2))
    return myG
    
def computeModularityUnd(modulesOnClust):
    
    G = SparseGRAPH(modulesOnClust)
    md = np.sum(G*(w_ij - modMat))

    del G
    
    gc.collect()

    return md
    
def myCostJaya(pop): #
    modularity = 0
    sortedpop = np.argsort(pop)
    modulesOnClusters=[]
    temp = []
    for i in sortedpop:
        if i < nModules:
            temp.append(i)
        else:
            modulesOnClusters.append(temp)
            temp = []
    if sortedpop[-1]<nModules:
        modulesOnClusters.append(temp)
        
    modularity = computeModularityUnd(modulesOnClusters)
    
    modularity = 1/(2*m) * modularity
    
    return(modularity)






def single():
    
    pop = [np.random.random() for _ in range(nModules+nCluster-1)]

    return [pop, myCostJaya(pop)]

def singlePop(_):

    return single()

def initialPopParallel():
    
    cores = mp.cpu_count()//1
    
    if algoMode == "sequential":
        cores = 1

    pool = Pool(cores)
    
    df_out = pool.map(singlePop,range(nPop))

    
    pool.close()
    pool.join()
    
    gc.collect()


    return df_out





def singleCrossOverOperator(offspring1,offspring2):
    
    
    np.random.seed(int.from_bytes(os.urandom(4), byteorder='little'))
    
    c=np.random.randint(1,len(offspring1[0]))
    
    x11=offspring1[0][0:c+1]
    x12=offspring1[0][c+1:]
   
    x21=offspring2[0][0:c+1]
    x22=offspring2[0][c+1:]
   
    
    off1=x11+x22
    off2=x21+x12
    
    offspring1[0]=off1
    offspring2[0]=off2
    
    offspring1[1] = myCostJaya(off1)
    offspring2[1] = myCostJaya(off2)
    
    return (offspring1,offspring2)



def RouletteWheelSelection_():
    
    np.random.seed(int.from_bytes(os.urandom(4), byteorder='little'))
    
    r=np.random.random()
    c=np.cumsum(Probabilities)
    i=np.where(r<=c)
    if len(i[0])==0:
        i=6
    else:
        i=i[0][0]
    return(i)


def SingleCrossOver():
    
    np.random.seed(int.from_bytes(os.urandom(4), byteorder='little'))
    
    parent1 = population[RouletteWheelSelection_()]
    parent2 = population[RouletteWheelSelection_()] 
    
    offspring1, offspring2 = singleCrossOverOperator(parent1,parent2)
    
    return (offspring1,offspring2)




def SingleCrossOver_(_):
    
    
    return SingleCrossOver()
    


def ParallelCrossOver():
    
    cores = mp.cpu_count()//1
    
    if algoMode == "sequential":
        cores = 1
    
    if crossNumber<cores:
        cores = crossNumber

    pool = Pool(cores)
    
    
    
    df_out = pool.map(SingleCrossOver_,range(crossNumber))
    
    pool.close()
    pool.join()

    
    df_out_ = [item for sublist in df_out for item in sublist]
    
    gc.collect()

    return df_out_





def SingleMutationOperator(parent):
    
    np.random.seed(int.from_bytes(os.urandom(4), byteorder='little'))
    
    offspring = [[],0]
    
    place2Mutate=np.random.choice(range(len(parent[0])),1)
    place2Mutate=place2Mutate[0]
    child=copy.deepcopy(parent)
    RAND=np.random.random()
    if RAND<0.2:
        #print("case1")
        child[0]=np.delete(parent[0],place2Mutate)
        child[0]=np.insert(child[0],np.random.randint(0, len(parent[0])-1),np.random.random())

    elif 0.2<=RAND<10.6:
        #print("case2")
        nn=len(parent[0])-1
        ip=np.random.choice(nn,2,replace=False)
        #print(ip)
        i1=ip[0]
        i2=ip[1]
        child=copy.deepcopy(parent)
        child[0][i1]=parent[0][i2]
        child[0][i2]=parent[0][i1] 
        child[0] = np.array(child[0])
    #else:
        #print("case3")
        #i=np.random.choice(range(len(parent[0])-1),2,replace=False)
        #i1=min(i)
        #i2=max(i)
        #child[0][i1:i2]=parent[0][i1:i2][::-1]
        #child[0] = np.array(child[0])
    # Decode and Calculate the Cost
    modularity = myCostJaya(child[0])
    #Update the population
    offspring[0] = child[0].tolist()
    offspring[1] = modularity
    return offspring




def SingleMutation():
    
    np.random.seed(int.from_bytes(os.urandom(4), byteorder='little'))
    
    parent = population[RouletteWheelSelection_()]
    
    offspring = SingleMutationOperator(parent)
    
    return offspring




def SingleMutation_(_):
    
    
    return SingleMutation()
    


def ParallelMutation():
    
    cores = mp.cpu_count()//1
    
    if algoMode == "sequential":
        cores = 1
    

    pool = Pool(cores)
    
    
    
    df_mut = pool.map(SingleMutation_,range(muteNumber))
    
    pool.close()
    pool.join()
    
    gc.collect()
    return df_mut







def SingleJAYAOperator(parent):
    
    r1 = 0.4
    r2 = 0.4
    child = [[],0]
    
    for i in range(len(parent[0])):
        child[0].append (parent[0][i] + r1 * (gBest[0][i] - abs(parent[0][i])) - r2 * (gWorst[0][i] - abs(parent[0][i])))
    modularity = myCostJaya(child[0])
    child[1] = modularity
    
    return(child)


def SingleJAYA():
    
    np.random.seed(int.from_bytes(os.urandom(4), byteorder='little'))
    
    parent = population[RouletteWheelSelection_()]
    
    offspring = SingleJAYAOperator(parent)
    
    return offspring


def SingleJAYA_(_):
    
    
    return SingleJAYA()
    

def ParallelJAYA():
    
    cores = mp.cpu_count()//1
    
    if algoMode == "sequential":
        cores = 1

    pool = Pool(cores)
    
    df_JAYA = pool.map(SingleJAYA_,range(muteNumber))
    
    pool.close()
    pool.join()

    gc.collect()
    
    return df_JAYA


def GA():
    
    global population, Probabilities
    
    tic = time.time()
    objective = 0
    miyu = 10
    clusters = []
    
    #%% Initialization
    '''
    Answer representation is here for future reference:
        |0.013|0.411|0.005|0.101|0.131 ....|0.433|
        length: number of modules + number of clusters - 1
        decoding guide: VRP-like
        use arg sort
        The reason I am using this representation is that JAYA is a continuous algorithm
    '''
    mutation_st = time.time()
    population = initialPopParallel()
    print("population init done!", time.time()-mutation_st, "secs")
    # Sort the Population
    sortedPopulation=copy.deepcopy(population)
    sortedPopulation.sort(key=lambda x: x[1], reverse = 1)
    population = sortedPopulation
    gBest = sortedPopulation[0]
    gWorst = sortedPopulation[-1]
    #%% Main Loop
    non_improved_iter_count = 0
    old_best = -1e10
    iternum = 0
    while time.time()-tic < timeLimit:
        gc.collect()
        Newpop=[]
        # Selecet Elite Parents and move them to next generation
        nElite=int(nPop*elitismProb)
        for i in range(nElite):
             Newpop.append(sortedPopulation[i])
        print("elites done!")        
        # Select Parents to Crossover and Mutation
        Probabilities=[]
        WorstCost=sortedPopulation[-1][1]
        for i in range(len(sortedPopulation)):
             temp=np.exp(-beta*sortedPopulation[i][1]/(abs(WorstCost)+0.000000000001))
             Probabilities.append(temp)
        Probabilities = [float(i)/sum(Probabilities) for i in Probabilities]
        # Crossover
        crossover_st = time.time()
        print("starting crossover...!")   
        offsprngs = ParallelCrossOver()
        print("crossover done!:", time.time()-crossover_st, "secs")
        Newpop = Newpop + offsprngs

        
        # Mutation
        mutation_st = time.time()
        print("starting mutation...!")   
        mutlist = ParallelMutation()
        print(" mutation done!...",time.time()-mutation_st, "secs")
        
        Newpop = Newpop + mutlist
        
        
        population=copy.deepcopy(Newpop)
        sortedPopulation=copy.deepcopy(population)
        sortedPopulation.sort(key=lambda x: x[1], reverse=1)
        sortedPopulation = sortedPopulation[:2*nPop]
        population = sortedPopulation
        #print("total pop_size before next generation:", len(population))
        iternum = iternum + 1
        BestSol=sortedPopulation[0]
        BestCost=BestSol[1]
        delta = BestCost-old_best
        
        if delta < tolerance:
            non_improved_iter_count = non_improved_iter_count + 1
        else:
            non_improved_iter_count = 0
            
        old_best = BestCost
        
        #print(iter, BestCost, delta, non_improved_iter_count)
        with open('ParallelAlgorithms/results_Undirected/GA_{}_graph'.format(software) + "_" + algoMode + "_" + str(nCluster), 'a+') as f:
            f.write(str(iternum)+'\t' + str(time.time()-tic) + '\t' + str(BestCost) + '\t' + str(delta) + '\t' + str(non_improved_iter_count) + '\n')
        #if time.time()-tic > 750:
            #break 
        #if non_improved_iter_count > patience:
            #break
        gc.collect()
        print("sorted pop memory usage: ", round(getsizeof(sortedPopulation) / 1024 / 1024,2))
        print("pop memory usage: ", round(getsizeof(population) / 1024 / 1024,2))
    return(BestCost, sortedPopulation[0][0])



def HYGAR():
    
    global population, Probabilities, gBest, gWorst
    
    tic = time.time()
    objective = 0
    miyu = 10
    clusters = []
    
    #%% Initialization
    '''
    Answer representation is here for future reference:
        |0.013|0.411|0.005|0.101|0.131 ....|0.433|
        length: number of modules + number of clusters - 1
        decoding guide: VRP-like
        use arg sort
        The reason I am using this representation is that JAYA is a continuous algorithm
    '''
    mutation_st = time.time()
    population = initialPopParallel()
    print("population init done!", time.time()-mutation_st, "secs")
    # Sort the Population
    sortedPopulation=copy.deepcopy(population)
    sortedPopulation.sort(key=lambda x: x[1], reverse = 1)
    population = sortedPopulation
    gBest = sortedPopulation[0]
    gWorst = sortedPopulation[-1]
    #%% Main Loop
    non_improved_iter_count = 0
    old_best = -1e10
    iternum = 0
    while time.time()-tic < timeLimit:
        gc.collect()
        Newpop=[]
        # Selecet Elite Parents and move them to next generation
        nElite=int(nPop*elitismProb)
        for i in range(nElite):
             Newpop.append(sortedPopulation[i])
        print("elites done!")        
        # Select Parents to Crossover and Mutation
        Probabilities=[]
        WorstCost=sortedPopulation[-1][1]
        for i in range(len(sortedPopulation)):
             temp=np.exp(-beta*sortedPopulation[i][1]/(abs(WorstCost)+0.000000000001))
             Probabilities.append(temp)
        Probabilities = [float(i)/sum(Probabilities) for i in Probabilities]
        # Crossover
        crossover_st = time.time()
        print("starting crossover...!")   
        offsprngs = ParallelCrossOver()
        print("crossover done!:", time.time()-crossover_st, "secs")
        Newpop = Newpop + offsprngs

        
        # Mutation
        mutation_st = time.time()
        print("starting mutation...!")   
        mutlist = ParallelMutation()
        print(" mutation done!...",time.time()-mutation_st, "secs")
        
        Newpop = Newpop + mutlist

        
        # JAYA
        JAYA_st = time.time()
        print("starting JAYA...!")   
        JAYAlist = ParallelJAYA()
        print("JAYA done!...",time.time()-JAYA_st, "secs")
        
        Newpop = Newpop + JAYAlist
        

        
        population=copy.deepcopy(Newpop)
        sortedPopulation=copy.deepcopy(population)
        sortedPopulation.sort(key=lambda x: x[1], reverse=1)
        sortedPopulation = sortedPopulation[:2*nPop]
        population = sortedPopulation
        gBest = sortedPopulation[0]
        gWorst = sortedPopulation[-1]

        #print("total pop_size before next generation:", len(population))
        iternum = iternum + 1
        BestSol=sortedPopulation[0]
        BestCost=BestSol[1]
        delta = BestCost-old_best
        
        if delta < tolerance:
            non_improved_iter_count = non_improved_iter_count + 1
        else:
            non_improved_iter_count = 0
            
        old_best = BestCost
        
        #print(iter, BestCost, delta, non_improved_iter_count)
        with open('ParallelAlgorithms/results_Undirected/HYGAR_{}_graph'.format(software) + "_" + algoMode + "_" + str(nCluster), 'a+') as f:
            f.write(str(iternum)+'\t' + str(time.time()-tic) + '\t' + str(BestCost) + '\t' + str(delta) + '\t' + str(non_improved_iter_count) + '\n')
        #if time.time()-tic > 750:
            #break 
        #if non_improved_iter_count > patience:
            #break
        gc.collect()
    return(BestCost, sortedPopulation[0][0])




def DecodeCluster(solution_representation):
    
    from itertools import groupby
    global cl_indexes
    
    tot_clusters = nCluster
    
    tot_items = len(CodeList)
    
    sorted_items = np.argsort(solution_representation).tolist()
    
    cl_indexes = [tot_items+i for i in range(tot_clusters-1)]
    
    def split_condition(x):
        return x in cl_indexes
    
    grouper = groupby(sorted_items, key=split_condition)
    
    
    res = dict(enumerate((list(j) for i, j in grouper if not i), 0))
    
    return res
    

def WriteConfigFile(cluster_dict):
    
    with open('warm_start/c_{}_{}.rsf'.format(software,nCluster), 'w') as f:
        for key in cluster_dict:
            for itm in cluster_dict[key]:
                my_line = "contain" + " " + str(key) + " " + CodeList[itm] + "\n"
                f.write(my_line)
        
    f.close()
        
        
        
def findOptimalSolutionWithInitialSolution():
    
    mdl = Model('MIP')
            
    nCodes = len(CodeList)

    y = mdl.binary_var_dict([(i,j) for i in range(nCodes) for j in range(nCluster)], name='y')
    z = mdl.binary_var_dict([(i,k) for i in range(nCodes) for k in range(nCodes)], name='z')
        
    #mdl.maximize(mdl.sum(z[i,k]*(DependencyMatrix[d][i][k]-(dOutArray[d][i]*dInArray[d][k]/nDependecies[d]))/nDependecies[d] for i in range(nCodes) for k in range(nCodes) for d in range(len(Dependencies))))           
      
    mdl.maximize(mdl.sum(z[i,k]*((DependencyMatrix[0][i][k]-(dOutArray[0][i]*dInArray[0][k]/nDependecies[0]))/nDependecies[0]) for i in range(nCodes) for k in range(nCodes)))
        
    #Constraints
    mdl.add_constraints(mdl.sum(y[i,j] for j in range(maxClusters)) == 1 for i in range(nCodes)) 
    mdl.add_constraints(y[i,j] - y[k,j] + z[i,k] <= 1 for i in range(nCodes) for k in range(nCodes) for j in range(nCluster)) 
    mdl.add_constraints(y[i,j] + y[k,j] - z[i,k] <= 1 for i in range(nCodes) for k in range(nCodes) for j in range(nCluster)) 
    #mdl.add_constraints(y[i,j] == 1 for i in range(nCodes) for j in range(maxClusters) if assignedClusters[i] == j)
    
    warmstart=mdl.new_solution()
    for j in range(nCluster):
        for i in range(nCodes):  
            if assignedClusters[i] == j:
                warmstart.add_var_value(y[i,j],1)
            else:
                warmstart.add_var_value(y[i,j],0)
    #warmstart.add_var_value(nbbus30,0)
    mdl.add_mip_start(warmstart)

    
    #mdl.set_results_stream(None)
    #mdl.parameters.mip.tolerances.mipgap = 0.005
    #mdl.parameters.timelimit=21600 #time limit

    #mdl.export("lpex1.lp")
    solution = mdl.solve(log_output= "cplex_logs/warm_start_{}_{}.txt".format(software,nCluster))
    mdl.parameters.threads.set(64)
    mdl.set_time_limit(900)
    #print(solution.solve_status) #if it says feasible, it is not optimal
    obj = solution.get_objective_value()
    mdl.solve_details
    print(obj)
    
    YSol = [y[i,j].solution_value for i in range(nCodes) for j in range(nCluster)]   
    
    ZSol = [z[i,k].solution_value for i in range(nCodes) for k in range(nCodes)] 
    
    data = np.array(YSol)
    shape = (nCodes, nCluster)
    data = data.reshape(shape)
    
    data2 = np.array(ZSol)
    shape = (nCodes, nCodes)
    data2 = data2.reshape(shape)
    
    mdl.end
    
    my_dct = {"YSol":data,
              "Zsol":data2}
    
    pickle.dump(my_dct, open("cplex_solutions/WarmSolution_{}_{}.pkl".format(), "wb"))
    
    return print("Warm Start Solution Finished...")

def findOptimalSolution():
    
    mdl = Model('MIP')
        
    nCodes = len(CodeList)

    y = mdl.binary_var_dict([(i,j) for i in range(nCodes) for j in range(nCluster)], name='y')
    z = mdl.binary_var_dict([(i,k) for i in range(nCodes) for k in range(nCodes)], name='z')
        
    #mdl.maximize(mdl.sum(z[i,k]*(DependencyMatrix[d][i][k]-(dOutArray[d][i]*dInArray[d][k]/nDependecies[d]))/nDependecies[d] for i in range(nCodes) for k in range(nCodes) for d in range(len(Dependencies))))           
      
    mdl.maximize(mdl.sum(z[i,k]*((DependencyMatrix[0][i][k]-(dOutArray[0][i]*dInArray[0][k]/nDependecies[0]))/nDependecies[0]) for i in range(nCodes) for k in range(nCodes)))
        
    #Constraints
    mdl.add_constraints(mdl.sum(y[i,j] for j in range(maxClusters)) == 1 for i in range(nCodes)) 
    mdl.add_constraints(y[i,j] - y[k,j] + z[i,k] <= 1 for i in range(nCodes) for k in range(nCodes) for j in range(nCluster)) 
    mdl.add_constraints(y[i,j] + y[k,j] - z[i,k] <= 1 for i in range(nCodes) for k in range(nCodes) for j in range(nCluster)) 
    mdl.add_constraints(y[i,j] == 1 for i in range(nCodes) for j in range(maxClusters) if assignedClusters[i] == j)
    
    #mdl.set_results_stream(None)
    #mdl.parameters.mip.tolerances.mipgap = 0.005
    #mdl.parameters.timelimit=21600 #time limit

    #mdl.export("lpex1.lp")
    solution = mdl.solve(log_output= "cplex_logs/cold_start_{}_{}.txt".format(software,nCluster))
    mdl.parameters.threads.set(64)
    mdl.set_time_limit(900)
    #print(solution.solve_status) #if it says feasible, it is not optimal
    obj = solution.get_objective_value()
    mdl.solve_details
    print(obj)
    
    YSol = [y[i,j].solution_value for i in range(nCodes) for j in range(maxClusters)]   
    
    ZSol = [z[i,k].solution_value for i in range(nCodes) for k in range(nCodes)] 
    
    data = np.array(YSol)
    shape = (nCodes, maxClusters)
    data = data.reshape(shape)
    
    data2 = np.array(ZSol)
    shape = (nCodes, nCodes)
    data2 = data2.reshape(shape)
    
    mdl.end
    
    my_dct = {"YSol":data,
             "Zsol":data2}
    
    pickle.dump(my_dct, open("cplex_solutions/ColdSolution_{}_{}.pkl".format(), "wb"))
    
    return print("Cold Start Solution Finished...")




def readdata(dependencyFiles, inputFile):

    global Dependencies, CodeList, DependencyMatrix, nDependecies, dInArray, dOutArray, assignedClusters
    
    CodeList = []
    assignedClusters = []
    Dependencies = []
    DependencyMatrix = []
    nDependecies = []
    dInArray = []
    dOutArray = []
        
    with open(inputFile) as f:
        lines = f.readlines()
        
    for i in lines:
        strList = i.split()
        assignedClusters.append(int(strList[1]))
        CodeList.append(strList[2])
        
    #CodeList = np.array(CodeList)
    #CodeList = np.unique(CodeList)
        
    count = 0
    for j in dependencyFiles:
        tempMatrix = [ [0]*len(CodeList) for i in range(len(CodeList))]
        tempdIn = [0]*len(CodeList) 
        tempdOut = [0]*len(CodeList) 
        Dependencies.append([])
        with open(j) as f:
            lines = f.readlines()
        for i in lines:
            strList = i.split()
            #CodeList.append(strList[2])            
            Dependencies[count].append((strList[1], strList[2]))
            index1 = CodeList.index(strList[1])
            #index1, = np.where(CodeList == strList[1])
            index2 = CodeList.index(strList[2])
            #index2, = np.where(CodeList == strList[2])
            tempMatrix[index1][index2] = 1
            tempdIn[index2] +=1
            tempdOut[index1] +=1
        dInArray.append(tempdIn)
        dOutArray.append(tempdOut)
        DependencyMatrix.append(tempMatrix)
        nDependecies.append(len(Dependencies[count]))
        count += 1
        print("data is read for CPLEX")
        
    
    
    
    
    

##########################################


if __name__ == "__main__":

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
                                    for software in software_list:
                                        for algoMode in algoModes:
                                            for algorithm in algorithms:

                                                nCluster = runHeuristics(software)
                                                dependencyFile = "dataset/{}/{}-dependency.rsf".format(software,software)

                                                parser = RSFParser(dependencyFile)
                                                parser.parse_dependency_input_file(dependencyFile)

                                                w_ij = np.array(parser.dsm).astype(np.int16)

                                                print("weight matrix sparsity: ",1.0 - (np.count_nonzero(w_ij) / float(w_ij.size)))
                                                print("weight matrix memory usage: ", round(getsizeof(w_ij) / 1024 / 1024,2))

                                                d_i = parser.ID2name
                                                clustered_items = parser.clustered_items
                                                

                                                nModules = len(w_ij)

                                                timeLimit = nModules*5 

                                                d_i = np.zeros(nModules)
                                                for i in range(nModules):
                                                    d_i[i] = 0
                                                    for j in range(nModules):
                                                        d_i[i] += w_ij[i][j]
                                                        
                                                m = 0.5 * np.sum(d_i)                                                    
                                                modMat = np.matmul(d_i.reshape(1,-1).T,d_i.reshape(1,-1))
                                                modMat = modMat/np.sum(d_i)
                                                modMat = modMat.astype(np.float16)

                                                print("modularity matrix sparsity: ",1.0 - (np.count_nonzero(modMat) / float(modMat.size)))
                                                print("modularity graph memory usage: ", round(getsizeof(modMat) / 1024 / 1024,2))

                                                CodeList = list(parser.name2ID.keys())
                                                DependencyMatrix = [parser.dsm]
                                                nDependecies = [parser.dependency_count]
                                                #dInArray = [parser.d_in]
                                                #dOutArray = [parser.d_out]
                                                timeLimit = nModules*5 
                                                print(software, "is being solved", "within time limit of ", timeLimit)
                                                print(software, "has", nModules, "modules")
                                                start = time.time()
                                                if algorithm == "GA":
                                                    objectiveGAJAYA, clusters = GA()
                                                    cpuGAJAYA = time.time()-start
                                                    q=open("ParallelAlgorithms/results_Undirected/Results_{}.csv".format(software), "a+")
                                                    q.write(algoMode +" "+ algorithm +" "+str(objectiveGAJAYA) + ' ' + str(cpuGAJAYA) + '\n')
                                                    q.write(str(nPop) + ',' +str(crossProb) + ',' +str(crossRate) + ',' +str(muteProb) + ',' +str(muteRate) + ',' +str(elitismProb) + ',' +str(beta) + ',' + str(objectiveGAJAYA) + ',' + str(cpuGAJAYA) + '\n')
                                                    q.close()
                                                if algorithm == "HYGAR":
                                                    objectiveGAJAYA, clusters = HYGAR()
                                                    cpuGAJAYA = time.time()-start
                                                    q=open("ParallelAlgorithms/results_Undirected/Results_{}.csv".format(software), "a+")
                                                    q.write(algoMode +" "+ algorithm +" "+ str(objectiveGAJAYA) + ' ' + str(cpuGAJAYA) + '\n')
                                                    q.write(str(nPop) + ',' +str(crossProb) + ',' +str(crossRate) + ',' +str(muteProb) + ',' +str(muteRate) + ',' +str(elitismProb) + ',' +str(beta) + ',' + str(objectiveGAJAYA) + ',' + str(cpuGAJAYA) + '\n')
                                                    q.close()
                                                    

                                                #dec = DecodeCluster(clusters)
                                        #WriteConfigFile(dec)
                                        #dependencyFiles = ["dataset/{}/{}-dependency.rsf".format(software,software)]
                                        #readdata(dependencyFiles, 'warm_start/c_{}_{}.rsf'.format(software,nCluster))
                                        #findOptimalSolutionWithInitialSolution()
                                        #findOptimalSolution()
                                    

