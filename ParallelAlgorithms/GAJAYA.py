# -*- coding: utf-8 -*-
"""
Created on Wed Aug  4 19:28:59 2021

@author: Milad
"""
import numpy as np
import time
from allfunctions import *
import copy
global MaxIt, nPop, crossNumber, muteNumber, muteRate, elitismProb, beta, nCluster, nModules, w_ij, d_i, crossRate, Dependencies, CodeList, DependencyMatrix, nDependecies, dInArray, dOutArray



def GAJAYA():
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
    
    
    
    
    #population=[] #This part can be parallelized
    #for i in range(nPop): 
    #    # Get the solution of DP-RL
    #    pop = [np.random.random() for _ in range(nModules+nClusters-1)]
    #    modularity = myCostJaya(pop,inputdata)
    
    #    #Update the population
    #    population.append([pop,modularity])
     
    init = time.time()
    
    population = initialPopParallel()
        
    print("init pop time: ", time.time()-init)

    print("init pop size: ", len(population))
    
    
    # Sort the Population
    sortedPopulation=copy.deepcopy(population)
    sortedPopulation.sort(key=lambda x: x[1], reverse = 1)
    population = sortedPopulation
    gBest = sortedPopulation[0]
    gWorst = sortedPopulation[-1]
    #%% Main Loop
    for iter in range(MaxIt):
        Newpop=[]
        # Selecet Elite Parents and move them to next generation
        nElite=int(nPop*elitismProb)
        for i in range(nElite):
             Newpop.append(sortedPopulation[i])
                
        # Select Parents to Crossover and Mutation
        Probabilities=[]
        WorstCost=sortedPopulation[-1][1]
        for i in range(len(sortedPopulation)):
             temp=np.exp(-beta*sortedPopulation[i][1]/(abs(WorstCost)+0.000000000001))
             Probabilities.append(temp)
        Probabilities = [float(i)/sum(Probabilities) for i in Probabilities]
        # Crossover
        crossover_st = time.time()
        #for k in range(crossNumber): #Could be parallelized?
        #    parent1=population[RouletteWheelSelection(P)]
        #    parent2=population[RouletteWheelSelection(P)]            
        #    offspring1, offspring2=CrossoverJAYA(parent1,parent2,inputdata)
        #    Newpop.append(offspring1)
        #    Newpop.append(offspring2)
        offsprngs = applyCrossOverParallel(crossNumber, Probabilities, population, inputdata)
        print("crossover time:", time.time()-crossover_st)
        
        
        Newpop = Newpop + offsprngs
        print("total pop_size after crossover: ", len(Newpop))
        # Mutation
        mutation_st = time.time()
        #for k in range(muteNumber): #Could be parallelized?
        #    parent=population[RouletteWheelSelection(P)]
        #    offspring=MutationJAYA(parent,inputdata)
        #    Newpop.append(offspring)
        mutlist = applyMutationParallel(muteNumber, population, Probabilities, inputdata)
        print(" mutation_duration: ",time.time()-mutation_st)
        
    
        Newpop = Newpop + mutlist
        
        print("total pop_size after mutation: ", len(Newpop))    
        population=copy.deepcopy(Newpop)
        sortedPopulation=copy.deepcopy(population)
        sortedPopulation.sort(key=lambda x: x[1], reverse=1)
        sortedPopulation = sortedPopulation[:2*nPop]
        population = sortedPopulation
        print("total pop_size before next generation:", len(population))
        BestSol=sortedPopulation[0]
        BestCost=BestSol[1]
        # print(BestCost)
        with open('GAJAYA_graph' + str(nClusters), 'a+') as f:
            f.write(str(iter)+'\t' + str(time.time()-tic) + '\t' + str(BestCost) + '\n')
        if time.time()-tic > 9000:
            break 
    return(BestCost, sortedPopulation[0][0])
