from GA_Parser_Class_New import *
import time
import copy
import numpy as np
from sys import getsizeof
import gc
gc.collect()

import Operators

import globals

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
    population = Operators.SPM("initial_population")
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
    while time.time()-tic < globals.timeLimit:
        gc.collect()
        Newpop=[]
        # Selecet Elite Parents and move them to next generation
        nElite=int(globals.nPop*globals.elitismProb)
        for i in range(nElite):
             Newpop.append(sortedPopulation[i])
        print("elites done!")        
        # Select Parents to Crossover and Mutation
        Probabilities=[]
        WorstCost=sortedPopulation[-1][1]
        for i in range(len(sortedPopulation)):
             temp=np.exp(-globals.beta*sortedPopulation[i][1]/(abs(WorstCost)+0.000000000001))
             Probabilities.append(temp)
        Probabilities = [float(i)/sum(Probabilities) for i in Probabilities]
        # Crossover
        crossover_st = time.time()
        print("starting crossover...!")   
        offsprngs = Operators.SPM("crossover")
        print("crossover done!:", time.time()-crossover_st, "secs")
        Newpop = Newpop + offsprngs

        
        # Mutation
        mutation_st = time.time()
        print("starting mutation...!")   
        mutlist = Operators.SPM("mutation")
        print(" mutation done!...",time.time()-mutation_st, "secs")
        
        Newpop = Newpop + mutlist
        
        
        population=copy.deepcopy(Newpop)
        sortedPopulation=copy.deepcopy(population)
        sortedPopulation.sort(key=lambda x: x[1], reverse=1)
        sortedPopulation = sortedPopulation[:2*globals.nPop]
        population = sortedPopulation
        #print("total pop_size before next generation:", len(population))
        iternum = iternum + 1
        BestSol=sortedPopulation[0]
        BestCost=BestSol[1]
        delta = BestCost-old_best
        
        if delta < globals.tolerance:
            non_improved_iter_count = non_improved_iter_count + 1
        else:
            non_improved_iter_count = 0
            
        old_best = BestCost
        
        #print(iter, BestCost, delta, non_improved_iter_count)
        with open('{}/GA_{}_graph'.format(globals.logging_directory,globals.software) + "_" + globals.algoMode + "_" + str(globals.nCluster), 'a+') as f:
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
    population = Operators.SPM("initial_population")
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
    while time.time()-tic < globals.timeLimit:
        gc.collect()
        Newpop=[]
        # Selecet Elite Parents and move them to next generation
        nElite=int(globals.nPop*globals.elitismProb)
        for i in range(nElite):
             Newpop.append(sortedPopulation[i])
        print("elites done!")        
        # Select Parents to Crossover and Mutation
        Probabilities=[]
        WorstCost=sortedPopulation[-1][1]
        for i in range(len(sortedPopulation)):
             temp=np.exp(-globals.beta*sortedPopulation[i][1]/(abs(WorstCost)+0.000000000001))
             Probabilities.append(temp)
        Probabilities = [float(i)/sum(Probabilities) for i in Probabilities]
        # Crossover
        crossover_st = time.time()
        print("starting crossover...!")   
        offsprngs = Operators.SPM("crossover")
        print("crossover done!:", time.time()-crossover_st, "secs")
        Newpop = Newpop + offsprngs

        
        # Mutation
        mutation_st = time.time()
        print("starting mutation...!")   
        mutlist = Operators.SPM("mutation")
        print(" mutation done!...",time.time()-mutation_st, "secs")
        
        Newpop = Newpop + mutlist

        
        # JAYA
        JAYA_st = time.time()
        print("starting JAYA...!")   
        JAYAlist = Operators.SPM("JAYA")
        print("JAYA done!...",time.time()-JAYA_st, "secs")
        
        Newpop = Newpop + JAYAlist
        

        
        population=copy.deepcopy(Newpop)
        sortedPopulation=copy.deepcopy(population)
        sortedPopulation.sort(key=lambda x: x[1], reverse=1)
        sortedPopulation = sortedPopulation[:2*globals.nPop]
        population = sortedPopulation
        gBest = sortedPopulation[0]
        gWorst = sortedPopulation[-1]

        #print("total pop_size before next generation:", len(population))
        iternum = iternum + 1
        BestSol=sortedPopulation[0]
        BestCost=BestSol[1]
        delta = BestCost-old_best
        
        if delta < globals.tolerance:
            non_improved_iter_count = non_improved_iter_count + 1
        else:
            non_improved_iter_count = 0
            
        old_best = BestCost
        
        #print(iter, BestCost, delta, non_improved_iter_count)
        with open('{}/HYGAR_{}_graph'.format(globals.logging_directory,globals.software) + "_" + globals.algoMode + "_" + str(globals.nCluster), 'a+') as f:
            f.write(str(iternum)+'\t' + str(time.time()-tic) + '\t' + str(BestCost) + '\t' + str(delta) + '\t' + str(non_improved_iter_count) + '\n')
        #if time.time()-tic > 750:
            #break 
        #if non_improved_iter_count > patience:
            #break
        gc.collect()
    return(BestCost, sortedPopulation[0][0])
