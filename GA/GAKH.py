# -*- coding: utf-8 -*-
"""
Created on Wed Aug  4 19:28:59 2021

@author: Milad
"""
import numpy as np
from allfunctions import myCost, RouletteWheelSelection, Crossover, Mutation, Cumulative
import copy
import time
def GAKH(inputdata):
    tic = time.time()
    MaxIt, nPop, crossNumber, muteNumber, muteRate, elitismProb, beta, nClusters, nModules, w_ij, d_i, crossRate = inputdata
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
    for i in range(nPop):
        # Get the solution of DP-RL
        pop = [np.random.randint(0,nClusters-1) for i in range(nModules)]
        modularity = myCost(pop,inputdata)
    
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
        # Crossover (Cumulative Motion)
        chbest = population[0]
        chworst = population[-1]
            
        for k in range(crossNumber):
            chi=population[RouletteWheelSelection(P)]
            chj=population[RouletteWheelSelection(P)]            
            chibest = chi
            chjbest = chj
            chiworst = chi
            chjworst =chj
            X,Y,A,B,K,Z = Cumulative(chi,chj,chibest,chiworst,chjbest,chjworst,chbest,chworst, inputdata)
            
            Newpop.append(X)
            Newpop.append(Y)
            Newpop.append(A)
            Newpop.append(B)
            Newpop.append(K)
            Newpop.append(Z)
            
        # Mutation (Local Movement)
        for k in range(muteNumber):
            chi=population[RouletteWheelSelection(P)]
            offspring=Mutation(chi,inputdata)
            Newpop.append(offspring)
            offspring=Mutation(offspring,inputdata)
            Newpop.append(offspring)
            offspring=Mutation(chbest,inputdata)
            Newpop.append(offspring)
        # Random Diffusion
        
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