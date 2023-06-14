import os

def initialize():
    global  nPop, crossNumber, muteNumber, muteRate, \
        elitismProb, beta, nCluster, nModules, w_ij, d_i, crossRate, \
        Dependencies, CodeList, DependencyMatrix, nDependecies,\
        algoMode, software, modMat, m, timeLimit, tolerance,logging_directory

    tolerance = 1e-6
    
    logging_directory = 'ParallelAlgorithms/Logs/'
    os.makedirs(logging_directory, exist_ok=True)
    if os.path.exists(logging_directory):
        print(f"Directory '{logging_directory}' created successfully or already exists.")
    else:
        print(f"Failed to create directory '{logging_directory}'.")