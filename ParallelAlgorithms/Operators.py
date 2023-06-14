from GA_Parser_Class_New import *
import numpy as np
from multiprocessing import Pool
import multiprocessing as mp
import copy
import os
import numpy as np
import itertools
import gc

import globals

def SparseGRAPH(clst_cnfg):

    myG = np.zeros((globals.nModules,globals.nModules)).astype(np.int16)
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
    md = np.sum(G*(globals.w_ij - globals.modMat))

    del G
    
    gc.collect()

    return md
    
def myCostJaya(pop): #
    modularity = 0
    sortedpop = np.argsort(pop)
    modulesOnClusters=[]
    temp = []
    for i in sortedpop:
        if i < globals.nModules:
            temp.append(i)
        else:
            modulesOnClusters.append(temp)
            temp = []
    if sortedpop[-1]<globals.nModules:
        modulesOnClusters.append(temp)
        
    modularity = computeModularityUnd(modulesOnClusters)
    
    modularity = 1/(2*globals.m) * modularity
    
    return(modularity)



def RouletteWheelSelection_():
    
    from Algorithms import Probabilities

    np.random.seed(int.from_bytes(os.urandom(4), byteorder='little'))
    
    r=np.random.random()
    c=np.cumsum(Probabilities)
    i=np.where(r<=c)
    if len(i[0])==0:
        i=6
    else:
        i=i[0][0]
    return(i)



def single(_):
    
    pop = [np.random.random() for _ in range(globals.nModules+globals.nCluster-1)]

    return [pop, myCostJaya(pop)]


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

def SingleCrossOver(_):
    from Algorithms import population
    np.random.seed(int.from_bytes(os.urandom(4), byteorder='little'))
    
    parent1 = population[RouletteWheelSelection_()]
    parent2 = population[RouletteWheelSelection_()] 
    
    offspring1, offspring2 = singleCrossOverOperator(parent1,parent2)
    
    return (offspring1,offspring2)



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




def SingleMutation(_):

    from Algorithms import population

    np.random.seed(int.from_bytes(os.urandom(4), byteorder='little'))
    
    parent = population[RouletteWheelSelection_()]
    
    offspring = SingleMutationOperator(parent)
    
    return offspring



def SingleJAYAOperator(parent):
    from Algorithms import gBest, gWorst
    r1 = 0.4
    r2 = 0.4
    child = [[],0]
    
    for i in range(len(parent[0])):
        child[0].append (parent[0][i] + r1 * (gBest[0][i] - abs(parent[0][i])) - r2 * (gWorst[0][i] - abs(parent[0][i])))
    modularity = myCostJaya(child[0])
    child[1] = modularity
    
    return(child)


def SingleJAYA(_):
    from Algorithms import population
    
    np.random.seed(int.from_bytes(os.urandom(4), byteorder='little'))
    
    parent = population[RouletteWheelSelection_()]
    
    offspring = SingleJAYAOperator(parent)
    
    return offspring







def SPM(operator_name):
    
    cores = mp.cpu_count()//1
    
    if globals.algoMode == "sequential":
        cores = 1
    

    if operator_name == "initial_population":

        pool = Pool(cores)

        df_SPM = pool.map(single,range(globals.nPop))

        pool.close()
        
        pool.join()
    

    if operator_name == "crossover":

        if globals.crossNumber<cores:

            cores = globals.crossNumber

        pool = Pool(cores)
    
        df_SPM = pool.map(SingleCrossOver,range(globals.crossNumber))
    
        pool.close()
        pool.join()

        df_SPM = [item for sublist in df_SPM for item in sublist]


    if operator_name == "mutation":

        if globals.muteNumber<cores:

            cores = globals.muteNumber

        pool = Pool(cores)
    
        df_SPM = pool.map(SingleMutation,range(globals.muteNumber))
    
        pool.close()
        pool.join()


    if operator_name == "JAYA":

        if globals.muteNumber<cores:

            cores = globals.muteNumber

        pool = Pool(cores)
    
        df_SPM =  pool.map(SingleJAYA,range(globals.muteNumber))
    
        pool.close()
        pool.join()

    return df_SPM
