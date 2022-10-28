# -*- coding: utf-8 -*-
"""
Created on Wed Aug  4 19:28:59 2021

@author: Milad
"""
import numpy as np
import time
from allfunctions import myCost, RouletteWheelSelection, Crossover, Mutation, myCostJaya, CrossoverJAYA, MutationJAYA, Jaya
import copy
def HYGARII(inputdata):
    tic = time.time()
    MaxIt, MaxDuration, nPop, crossNumber, muteNumber, muteRate, elitismProb, beta, nClusters, nModules, w_ij, d_i, crossRate, Dependencies, CodeList, DependencyMatrix, nDependecies, dInArray, dOutArray, isDirected, outFileName = inputdata
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
    
    population=[]
    for _ in range(nPop):
        # Get the solution of DP-RL
        pop = [np.random.random() for _ in range(nModules+nClusters-1)]
        modularity = myCostJaya(pop,inputdata)
    
        #Update the population
        population.append([pop,modularity])
             
    # Sort the Population
    sortedPopulation=copy.deepcopy(population)
    sortedPopulation.sort(key=lambda x: x[1], reverse = 1)
    population = sortedPopulation
    gBest = sortedPopulation[0]
    gWorst = sortedPopulation[-1]
    #%% Main Loop
    for iteration in range(MaxIt):
        tic_iter = time.time()
        Newpop=[]
        # Selecet Elite Parents and move them to next generation
        nElite=int(nPop*elitismProb)
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
            offspring1, offspring2=CrossoverJAYA(parent1,parent2,inputdata)
            Newpop.append(offspring1)
            Newpop.append(offspring2)
            offspring1, offspring2 = Jaya(offspring1, inputdata, gBest, gWorst),Jaya(offspring2, inputdata, gBest, gWorst)
            Newpop.append(offspring1)
            Newpop.append(offspring2)
        # Mutation
        for _ in range(muteNumber):
            parent=population[RouletteWheelSelection(P)]
            offspring=MutationJAYA(parent,inputdata)
            Newpop.append(offspring)
            offspring = Jaya(offspring, inputdata, gBest, gWorst)
            Newpop.append(offspring)

        # JAYA
        Newpop.sort(key=lambda x: x[1], reverse=1)
        best = Newpop[0]
        worst = Newpop [-1]
        for k in range(40):
            parent=Newpop[k]
            offspring = Jaya(parent, inputdata, best, worst)
            Newpop.append(offspring)
            
        population=copy.deepcopy(Newpop)
        sortedPopulation=copy.deepcopy(population)
        sortedPopulation.sort(key=lambda x: x[1], reverse=1)
        gBest = sortedPopulation[0]
        gWorst = sortedPopulation[-1]
        sortedPopulation = sortedPopulation[:2*nPop]
        population = sortedPopulation
        BestSol=sortedPopulation[0]
        BestCost=BestSol[1]
        # print(BestCost)
        with open(outFileName + "-HYGARII.csv", 'a+') as f:
            toc_iter = time.time()
            f.write(str(iteration)+ ',' + str(toc_iter-tic_iter) + "," + str(toc_iter-tic) + ',' + str(BestCost) + '\n')
        if time.time()-tic > MaxDuration:
            break
    
    return(BestCost, sortedPopulation[0][0])
