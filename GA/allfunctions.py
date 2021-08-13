# -*- coding: utf-8 -*-
"""
Created on Thu Aug  5 01:48:27 2021

@author: Milad
"""
import numpy as np
import copy
#%% Modularity
def myCost(pop,inputdata):
    MaxIt, nPop, crossNumber, muteNumber, muteRate, elitismProb, beta, nClusters, nModules, w_ij, d_i = inputdata
    modularity = 0
    modulesOnClusters = []
    m = 0.5 * np.sum(d_i)
    for l in range(nClusters):
        temp =[]
        for k in range(len(pop)):
            if pop[k] == l:
                temp.append(k)
        modulesOnClusters.append(temp)
        for i in modulesOnClusters[l]:
            for j in modulesOnClusters[l]:
                modularity += w_ij[i][j] - d_i[i]*d_i[j]/(2*m)
    modularity = 1/(2*m) * modularity
    return(modularity)
#%% RolletteWheel
def RouletteWheelSelection(P):
     r=np.random.random()
     c=np.cumsum(P)
     i=np.where(r<=c)
     if len(i[0])==0:
          i=6
     else:
          i=i[0][0]
     return(i)
#%% Crossover
def Crossover(parent1,parent2,inputdata):
    MaxIt, nPop, crossNumber, muteNumber, muteRate, elitismProb, beta, nClusters, nModules, w_ij, d_i = inputdata
    offspring1=copy.deepcopy(parent1)
    offspring2=copy.deepcopy(parent2)
    c=np.random.randint(1,len(parent1[0])-1)
    x11=offspring1[0][0:c+1]
    x12=offspring1[0][c+1:]
   
    x21=offspring2[0][0:c+1]
    x22=offspring2[0][c+1:]
   
    
    off1=x11+x22
    off2=x21+x12
    offspring1[0]=off1
    offspring2[0]=off2
    off1=offspring1[0]    
    modularity = myCost(off1,inputdata)
    offspring1[1]=modularity
    off2=offspring2[0]    
    modularity = myCost(off2,inputdata)
    offspring2[1]=modularity
    
    return(offspring1,offspring2)
#%% Mutation
def Mutation(parent,inputdata):
    
    MaxIt, nPop, crossNumber, muteNumber, muteRate, elitismProb, beta, nClusters, nModules, w_ij, d_i = inputdata
    offspring = [[],0]
    if np.random.random()<0.1:
        child = [[], 0]
        pop = [np.random.randint(0,nClusters-1) for i in range(nModules)]
        child[0] = np.array(pop)
    else:
        place2Mutate=np.random.choice(range(nModules),1)
        place2Mutate=place2Mutate[0]
        child=copy.deepcopy(parent)
        RAND=np.random.random()
        if RAND<0.2:
            child[0]=np.delete(parent[0],place2Mutate)
            child[0]=np.insert(child[0],np.random.choice(len(child[0])),np.random.randint(0, nClusters-1,1)[0])
        elif 0.2<=RAND<0.4:
            child[0] = np.flip(parent[0])
        elif 0.4<=RAND<0.6:
            nn=len(parent[0])
            ip=np.random.choice(nn,2,replace=False)
            i1=ip[0]
            i2=ip[1]
            child=copy.deepcopy(parent)
            child[0][i1]=parent[0][i2]
            child[0][i2]=parent[0][i1] 
            child[0] = np.array(child[0])
        else:
            i=np.random.choice(range(len(parent[0])),2,replace=False)
            i1=min(i)
            i2=max(i)
            child[0][i1:i2]=parent[0][i1:i2][::-1]
            child[0] = np.array(child[0])
    # Decode and Caclulate the Cost
    modularity = myCost(child[0],inputdata)
    #Update the population
    offspring[0] = child[0].tolist()
    offspring[1] = modularity
    return(offspring)