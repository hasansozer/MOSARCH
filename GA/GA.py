# -*- coding: utf-8 -*-
"""
Created on Wed Aug  4 19:28:59 2021

@author: Milad
"""
import numpy as np
from allfunctions import myCost, RouletteWheelSelection, Crossover, Mutation
import copy
import time
def GA(inputdata):
    tic = time.time()
    MaxIt, MaxDuration, nPop, crossNumber, muteNumber, muteRate, elitismProb, beta, nClusters, nModules, w_ij, d_i, crossRate, Dependencies, CodeList, DependencyMatrix, nDependecies, dInArray, dOutArray, outFileName = inputdata
    objective = 0
    clusters = []
    
    #%% Initialization
    '''
    Answer representation is here for future reference:
        |3|4|5|10|11 ....|3|
        length: number of modules
        number in between: The cluster that module is asssigned too
    '''
    
    population=[]
    for _ in range(nPop):
        # Get the solution of DP-RL
        pop = [np.random.randint(0,nClusters) for _ in range(nModules)]
        modularity = myCost(pop,inputdata)
    
        #Update the population
        population.append([pop,modularity])

    # Sort the Population
    sortedPopulation=copy.deepcopy(population)
    sortedPopulation.sort(key=lambda x: x[1], reverse = 1)
    population = sortedPopulation
    #%% Main Loop
    for iteration in range(MaxIt):
        tic_iter = time.time()
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
        for _ in range(crossNumber):
            parent1=population[RouletteWheelSelection(P)]
            parent2=population[RouletteWheelSelection(P)]            
            offspring1, offspring2=Crossover(parent1,parent2,inputdata)
            Newpop.append(offspring1)
            Newpop.append(offspring2)
        # Mutation
        for _ in range(muteNumber):
            parent=population[RouletteWheelSelection(P)]
            offspring=Mutation(parent,inputdata)
            Newpop.append(offspring)
        population=copy.deepcopy(Newpop)
        sortedPopulation=copy.deepcopy(population)
        sortedPopulation.sort(key=lambda x: x[1], reverse=1)
        sortedPopulation = sortedPopulation[:nPop]
        population = sortedPopulation
        BestSol=sortedPopulation[0]
        BestCost=BestSol[1]
        # print(BestCost)
        with open(outFileName + "-GA.csv", 'a+') as f:
            toc_iter = time.time()
            f.write(str(iteration) + ',' + str(toc_iter-tic_iter) + "," + str(toc_iter-tic) + ',' + str(BestCost) + '\n')
        if time.time()-tic > MaxDuration:
            break
    return(BestCost, sortedPopulation[0][0])
