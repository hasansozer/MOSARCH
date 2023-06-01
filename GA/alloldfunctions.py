"""
Helper functions for HYGARI, HYGARII before refactoring for HYGARIII
"""

import numpy as np
import copy
#%% Modularity
def myCost(pop,inputdata):
    MaxIt, MaxDuration, nPop, crossNumber, muteNumber, muteRate, elitismProb, beta, nClusters, nModules, w_ij, d_i, crossRate, Dependencies, CodeList, DependencyMatrix, nDependecies, dInArray, dOutArray, isDirected, outFileName = inputdata
    modularity = 0
    modulesOnClusters = []
    if isDirected == "directed":
        for l in range(nClusters):
            temp =[]
            for k in range(len(pop)):
                if pop[k] == l:
                    temp.append(k)
            modulesOnClusters.append(temp)
            for i in modulesOnClusters[l]:
                for j in modulesOnClusters[l]:
                    if i!=j:
                        modularity += (DependencyMatrix[0][i][j]-(dOutArray[0][i]*dInArray[0][j]/nDependecies[0]))/nDependecies[0]
    else:
        m = 0.5 * np.sum(d_i) + 0.00000001
        for l in range(nClusters):
            temp =[]
            for k in range(len(pop)):
                if pop[k] == l:
                    temp.append(k)
            modulesOnClusters.append(temp)
            for i in modulesOnClusters[l]:
                for j in modulesOnClusters[l]:
                    if i!=j:
                        modularity += w_ij[i][j] - d_i[i]*d_i[j]/(2*m)
        modularity = 1/(2*m) * modularity
    return(modularity)

#%% Modularity for JAYA
def myCostJaya(pop,inputdata):
    MaxIt, MaxDuration, nPop, crossNumber, muteNumber, muteRate, elitismProb, beta, nClusters, nModules, w_ij, d_i, crossRate, Dependencies, CodeList, DependencyMatrix, nDependecies, dInArray, dOutArray, isDirected, outFileName = inputdata
    modularity = 0
    modulesOnClusters = []
    sortedpop = np.argsort(pop)
    modulesOnClusters=[]
    temp = []

    if isDirected == "directed":
        for i in sortedpop:
            if i < nModules:
                temp.append(i)
            else:
                modulesOnClusters.append(temp)
                temp = []
        if sortedpop[-1]<nModules:
            modulesOnClusters.append(temp)

        for l in range(len(modulesOnClusters)):
            for i in modulesOnClusters[l]:
                for j in modulesOnClusters[l]:
                    if i!=j:
                        modularity += (DependencyMatrix[0][i][j]-(dOutArray[0][i]*dInArray[0][j]/nDependecies[0]))/nDependecies[0]
    else:
        for i in sortedpop:
            if i < nModules:
                temp.append(i)
            else:
                modulesOnClusters.append(temp)
                temp = []
        if sortedpop[-1]<nModules:
            modulesOnClusters.append(temp)
        m = 0.5 * np.sum(d_i) + 0.00000001
        for l in range(len(modulesOnClusters)):
            for i in modulesOnClusters[l]:
                for j in modulesOnClusters[l]:
                    if i!=j:
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
    MaxIt, MaxDuration, nPop, crossNumber, muteNumber, muteRate, elitismProb, beta, nClusters, nModules, w_ij, d_i, crossRate, Dependencies, CodeList, DependencyMatrix, nDependecies, dInArray, dOutArray, isDirected, outFileName = inputdata
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
    MaxIt, MaxDuration, nPop, crossNumber, muteNumber, muteRate, elitismProb, beta, nClusters, nModules, w_ij, d_i, crossRate, Dependencies, CodeList, DependencyMatrix, nDependecies, dInArray, dOutArray, isDirected, outFileName = inputdata
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

#%% CrossoverJAYA
def CrossoverJAYA(parent1,parent2,inputdata):
    MaxIt, MaxDuration, nPop, crossNumber, muteNumber, muteRate, elitismProb, beta, nClusters, nModules, w_ij, d_i, crossRate, Dependencies, CodeList, DependencyMatrix, nDependecies, dInArray, dOutArray, isDirected, outFileName = inputdata
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
    modularity = myCostJaya(off1,inputdata)
    offspring1[1]=modularity
    off2=offspring2[0]    
    modularity = myCostJaya(off2,inputdata)
    offspring2[1]=modularity
    
    return(offspring1,offspring2)
#%% Mutation
def MutationJAYA(parent,inputdata):
    MaxIt, MaxDuration, nPop, crossNumber, muteNumber, muteRate, elitismProb, beta, nClusters, nModules, w_ij, d_i, crossRate, Dependencies, CodeList, DependencyMatrix, nDependecies, dInArray, dOutArray, isDirected, outFileName = inputdata
    offspring = [[],0]
    if np.random.random()<0.1:
        child = [[], 0]
        pop = [np.random.random() for i in range(nModules+nClusters-1)]
        child[0] = np.array(pop)
    else:
        place2Mutate=np.random.choice(range(nModules),1)
        place2Mutate=place2Mutate[0]
        child=copy.deepcopy(parent)
        RAND=np.random.random()
        if RAND<0.2:
            child[0]=np.delete(parent[0],place2Mutate)
            child[0]=np.insert(child[0],np.random.choice(len(child[0])),np.random.randint(0, nClusters,1)[0])
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
    modularity = myCostJaya(child[0],inputdata)
    #Update the population
    offspring[0] = child[0].tolist()
    offspring[1] = modularity
    return(offspring)
#%% Cumulative Motion

def Cumulative(chi,chj,chibest,chiworst,chjbest,chjworst,chbest,chworst, inputdata):
    MaxIt, MaxDuration, nPop, crossNumber, muteNumber, muteRate, elitismProb, beta, nClusters, nModules, w_ij, d_i, crossRate, Dependencies, CodeList, DependencyMatrix, nDependecies, dInArray, dOutArray, isDirected, outFileName = inputdata
    # Calculate X
    if np.random.random() < crossRate:
        offspring1, offspring2=Crossover(chi,chj,inputdata)
    else:
        offspring1, offspring2 = chi,chj
        
    if offspring1[1]>offspring2[1]:
        temp = offspring1
    else:
        temp = offspring2
        
    if np.random.random() < crossRate:
        offspring1, offspring2=Crossover(chbest,chworst,inputdata)
    else:
        offspring1, offspring2 = chbest,chworst
    if offspring1[1]>offspring2[1]:
        best = offspring1
    else:
        best = offspring2
        
    if temp[1]>best[1]:
        X = temp
    else:
        X = best
    
    # Calclate Y
    if np.random.random() < crossRate:
        offspring1, offspring2=Crossover(chi,chj,inputdata)
        offspring3, offspring4=Crossover(chi,chbest,inputdata)
        offspring4, offspring5=Crossover(chj,chbest,inputdata)
    else:
        
        offspring1, offspring2=chi,chj
        offspring3, offspring4=chi,chbest
        offspring4, offspring5=chj,chbest
    offs = []
    offs.append(offspring1)
    offs.append(offspring2)
    offs.append(offspring3)
    offs.append(offspring4)
    offs.append(offspring5)
    for i in range(len(offs)-1):
        if offs[i][1]>offs[i+1][1]:
            temp = offs[i]
        else:
            temp = offs[i+1]
    offs = []
    offs.append(offspring1)
    offs.append(offspring2)                
    offspring3, offspring4=chi,chworst
    offspring44, offspring55=chj,chworst                    
    offs.append(offspring3)
    offs.append(offspring44)
    offs.append(offspring55)
    for i in range(len(offs)-1):
        if offs[i][1]>offs[i+1][1]:
            temp2 = offs[i]
        else:
            temp2 = offs[i+1]                
    if temp2[1]>temp[1]:
        Y = temp2
    else:
        Y = temp
    #Calculate A
    if np.random.random() < crossRate:
        offspring1, offspring2=Crossover(chi,chbest,inputdata)
    else:
        offspring1, offspring2=chi,chbest
    if offspring1[1] > offspring2[1]:
        temp = offspring1
    else:
        temp = offspring2
    
    if np.random.random() < crossRate:
        offspring1, offspring2=Crossover(chi,chworst,inputdata)
    else:
        offspring1, offspring2=chi,chworst            
    if offspring1[1] > offspring2[1]:
        temp2 = offspring1
    else:
        temp2 = offspring2            
    if temp2[1]>temp[1]:
        A = temp2
    else:
        A = temp

    #Calculate B
    if np.random.random() < crossRate:
        offspring1, offspring2=Crossover(chj,chbest,inputdata)
    else:
        offspring1, offspring2=chj,chbest
    if offspring1[1] > offspring2[1]:
        temp = offspring1
    else:
        temp = offspring2
    
    if np.random.random() < crossRate:
        offspring1, offspring2=Crossover(chj,chworst,inputdata)
    else:
        offspring1, offspring2=chj,chworst            
    if offspring1[1] > offspring2[1]:
        temp2 = offspring1
    else:
        temp2 = offspring2            
    if temp2[1]>temp[1]:
        B = temp2
    else:
        B = temp            
    worst = chiworst[1]
    best =  chibest[1]
    if X[1]>best:
        best = X[1]
        chibest = X
    if X[1]<worst:
        worst = X[1]
        chiworst = X
    if Y[1]>best:
        best = Y[1]
        chibest = Y
    if X[1]<worst:
        worst = Y[1]
        chiworst = Y                
    if A[1]>best:
        best = A[1]
        chibest = A
    if A[1]<worst:
        worst = A[1]
        chiworst = A                
    if B[1]>best:
        best = B[1]
        chibest = B
    if B[1]<worst:
        worst = B[1]
        chiworst = B
    worst = chjworst[1]
    best =  chjbest[1]
    if X[1]>best:
        best = X[1]
        chjbest = X
    if X[1]<worst:
        worst = X[1]
        chjworst = X
    if Y[1]>best:
        best = Y[1]
        chibest = Y
    if X[1]<worst:
        worst = Y[1]
        chjworst = Y                
    if A[1]>best:
        best = A[1]
        chjbest = A
    if A[1]<worst:
        worst = A[1]
        chjworst = A                
    if B[1]>best:
        best = B[1]
        chjbest = B
    if B[1]<worst:
        worst = B[1]
        chjworst = B
    #Calculate K
    if np.random.random() < crossRate:
        offspring1, offspring2=Crossover(chi,chibest,inputdata)
    else:
        offspring1, offspring2=chi,chibest
    if offspring1[1] > offspring2[1]:
        temp = offspring1
    else:
        temp = offspring2
    
    if np.random.random() < crossRate:
        offspring1, offspring2=Crossover(chi,chiworst,inputdata)
    else:
        offspring1, offspring2=chi,chiworst          
    if offspring1[1] > offspring2[1]:
        temp2 = offspring1
    else:
        temp2 = offspring2            
    if temp2[1]>temp[1]:
        K = temp2
    else:
        K = temp            
    #Calculate Z
    if np.random.random() < crossRate:
        offspring1, offspring2=Crossover(chj,chjbest,inputdata)
    else:
        offspring1, offspring2=chj,chjbest
    if offspring1[1] > offspring2[1]:
        temp = offspring1
    else:
        temp = offspring2
    
    if np.random.random() < crossRate:
        offspring1, offspring2=Crossover(chj,chjworst,inputdata)
    else:
        offspring1, offspring2=chj,chjworst          
    if offspring1[1] > offspring2[1]:
        temp2 = offspring1
    else:
        temp2 = offspring2            
    if temp2[1]>temp[1]:
        Z = temp2
    else:
        Z = temp    
    return(X,Y,A,B,K,Z)

#%% JAYA
def Jaya(parent,inputdata,best,worst):
    r1 = 0.4
    r2 = 0.4
    MaxIt, MaxDuration, nPop, crossNumber, muteNumber, muteRate, elitismProb, beta, nClusters, nModules, w_ij, d_i, crossRate, Dependencies, CodeList, DependencyMatrix, nDependecies, dInArray, dOutArray, isDirected, outFileName = inputdata
    child = [[],0]
    for i in range(len(parent[0])):
        child[0].append (parent[0][i] + r1 * (best[0][i] - abs(parent[0][i])) - r2 * (worst[0][i] - abs(parent[0][i])) )
    modularity = myCostJaya(child[0],inputdata)
    child[1] = modularity
    return(child)
