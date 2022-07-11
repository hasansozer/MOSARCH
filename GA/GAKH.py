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
    max_iterations, population_size, num_crossover, num_mutations, mutation_rate, elitism_probability, beta, num_clusters, num_modules, w_ij, d_i, crossover_rate, code_list, dependency_matrix, num_dependencies, d_in, d_out, max_duration = inputdata
    
    population=[]
    for i in range(population_size):
        # Get the solution of DP-RL
        pop = [np.random.randint(0,num_clusters) for _ in range(num_modules)]
        modularity = myCost(pop,inputdata)
    
        #Update the population
        population.append([pop,modularity])
             
    # Sort the Population
    sortedPopulation=copy.deepcopy(population)
    sortedPopulation.sort(key=lambda x: x[1], reverse = 1)
    population = sortedPopulation

    for iter in range(max_iterations):
        Newpop=[]
        # Select Elite Parents and move them to next generation
        nElite=int(population_size*elitism_probability)

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
            
        for _ in range(num_crossover):
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
        for _ in range(num_mutations):
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
        sortedPopulation = sortedPopulation[:population_size]
        population = sortedPopulation
        BestSol=sortedPopulation[0]
        BestCost=BestSol[1]

        
    return BestCost, sortedPopulation[0][0]
