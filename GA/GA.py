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
    max_iterations, population_size, num_crossover, num_mutations, mutation_rate, elitism_probability, beta, num_clusters, num_modules, w_ij, d_i, crossover_rate, code_list, dependency_matrix, num_dependencies, d_in, d_out, max_duration = inputdata

    population=[]
    for _ in range(population_size):
        # Get the solution of DP-RL
        pop = [np.random.randint(0,num_clusters) for _ in range(num_modules)]
        modularity = myCost(pop,inputdata)
    
        #Update the population
        population.append([pop,modularity])

    # Sort the Population
    sortedPopulation=copy.deepcopy(population)
    sortedPopulation.sort(key=lambda x: x[1], reverse = 1)
    population = sortedPopulation

    for _ in range(max_iterations):
        Newpop=[]
        # Selecet Elite Parents and move them to next generation
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
        # Crossover
        for _ in range(num_crossover):
            parent1=population[RouletteWheelSelection(P)]
            parent2=population[RouletteWheelSelection(P)]            
            offspring1, offspring2=Crossover(parent1,parent2,inputdata)
            Newpop.append(offspring1)
            Newpop.append(offspring2)
        # Mutation
        for _ in range(num_mutations):
            parent=population[RouletteWheelSelection(P)]
            offspring=Mutation(parent,inputdata)
            Newpop.append(offspring)

        population=copy.deepcopy(Newpop)
        sortedPopulation=copy.deepcopy(population)
        sortedPopulation.sort(key=lambda x: x[1], reverse=1)
        sortedPopulation = sortedPopulation[:population_size]
        population = sortedPopulation
        BestSol=sortedPopulation[0]
        BestCost=BestSol[1]

    return BestCost, sortedPopulation[0][0]
