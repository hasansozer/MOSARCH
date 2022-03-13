# -*- coding: utf-8 -*-
"""
Created on Wed Aug  4 19:28:59 2021

@author: Milad
"""
import numpy as np
import time
from allfunctions import myCost, RouletteWheelSelection, Crossover, Mutation, myCostJaya, CrossoverJAYA, MutationJAYA, Jaya
import copy
def GAJAYA(parser,inputdata):
    tic = time.time()
    MaxIt, nPop, crossNumber, muteNumber, muteRate, elitismProb, beta, nClusters, nModules, w_ij, d_i, crossRate = inputdata
    objective = 0
    clusters = []
    
    #%% Initialization
    '''
    Answer representation is here for future reference:
        |0.013|0.411|0.005|0.101|0.131 ....|0.433|
        length: number of modules + number of clusters - 1
        decoding guide: VRP-like
        use arg sort
        The reason I am using this repesntation is that JAYA is a continuous algorithm
    '''
    
    population=[]
    for i in range(nPop):
        # Get the solution of DP-RL
        pop = [np.random.random() for i in range(nModules+nClusters-1)]
        modularity = myCostJaya(parser,pop,inputdata)
    
        #Update the population
        population.append([pop,modularity])
             
    # Sort the Population
    sortedPopulation=copy.deepcopy(population)
    sortedPopulation.sort(key=lambda x: x[1], reverse = 1)
    population = sortedPopulation
    #%% Main Loop
    for iter in range(MaxIt):
        Newpop=[]
        # Selecet Elite Parents and move them to next generation
        nElite=int(nPop*elitismProb)
        nNonElite=nPop-nElite
        for i in range(nElite):
             Newpop.append(sortedPopulation[i])
        # Select Parents to Crossover and Mutation
        P=[]
        WorstCost=sortedPopulation[-1][1]
        for i in range(len(sortedPopulation)):
             temp=np.exp(-beta*sortedPopulation[i][1]/(abs(WorstCost)+0.000000000001))
             P.append(temp)
        temp=[]
        for i in range(len(P)):
             temp.append(P[i]/sum(P))
        P=temp
        # Crossover
        for k in range(crossNumber):
            parent1=population[RouletteWheelSelection(P)]
            parent2=population[RouletteWheelSelection(P)]            
            offspring1, offspring2=CrossoverJAYA(parent1,parent2,inputdata)
            Newpop.append(offspring1)
            Newpop.append(offspring2)
        # Mutation
        for k in range(muteNumber):
            parent=population[RouletteWheelSelection(P)]
            offspring=MutationJAYA(parent,inputdata)
            Newpop.append(offspring)
        # JAYA
        best = population[0]
        worst = population [-1]
        for k in range(20):
            parent=population[RouletteWheelSelection(P)]
            offspring = Jaya(parent, inputdata, best, worst)
            Newpop.append(offspring)
            
        population=copy.deepcopy(Newpop)
        sortedPopulation=copy.deepcopy(population)
        sortedPopulation.sort(key=lambda x: x[1], reverse=1)
        sortedPopulation = sortedPopulation[:nPop]
        population = sortedPopulation
        BestSol=sortedPopulation[0]
        BestCost=BestSol[1]
        print(BestCost)
        if time.time() - tic > 1000:
            break    
    return(BestCost, sortedPopulation[0][0])