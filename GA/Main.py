import argparse
from GA import GA
from GAKH import GAKH
from GAJAYA import GAJAYA
from GA_Parser_Class import *
import time
import numpy as np

def main(cmd_opt):
    max_iterations = cmd_opt['max_iterations']
    max_duration = cmd_opt['max_duration']
    population_size = cmd_opt['population_size']
    crossover_probability = cmd_opt['crossover_probability']
    crossover_rate = cmd_opt['crossover_rate']
    mutation_probability = cmd_opt['mutation_probability']
    mutation_rate = cmd_opt['mutation_rate']
    elitism_probability = cmd_opt['elitism_probability']
    beta = cmd_opt['betas']
    num_clusters = cmd_opt['num_clusters']
    np.random.seed(cmd_opt['seed'])


    parser = RSFParser()
    parser.parse_dependency_input_file(cmd_opt['dependency_file'])

    w_ij = np.array(parser.dsm).astype(int)
    d_i = parser.ID2name

    num_modules = len(w_ij)
    d_i = np.zeros(num_modules)
    for i in range(num_modules):
        d_i[i] = 0
        for j in range(num_modules):
            d_i[i] += w_ij[i][j]


    num_crossover = 2 * int(crossover_probability * population_size / 2)
    num_mutations  = int(mutation_probability * population_size)


    code_list = parser.name2ID.keys()
    dependency_matrix = parser.dsm
    num_dependencies = parser.dependency_count
    d_in = parser.d_in
    d_out = parser.d_out


    inputdata = max_iterations, population_size, num_crossover, num_mutations, mutation_rate, elitism_probability, beta, num_clusters, num_modules, w_ij, d_i, crossover_rate, code_list, dependency_matrix, num_dependencies, d_in, d_out, max_duration

    
    objective, clusters = None, None

    start = time.time()
    if cmd_opt['algorithm'] == 'GA':
        objective, clusters = GA(inputdata)
    elif cmd_opt['algorithm'] == 'GAKH':
        objective, clusters = GAKH(inputdata)
    elif cmd_opt['algorithm'] == 'HYGAR':
        objective, clusters = GAJAYA(inputdata)
    
    #print(objective)
    print(clusters)

    with open(cmd_opt['out_file'], "w+") as f:
        for item in clusters:
            pass
    

if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    # data args
    parser.add_argument('--dependency_file', type=str, help='Dependency file in .rsf format')
    parser.add_argument('--clustering_file', type=str, help='Clustering file in .rsf format')
    parser.add_argument('--algorithm', type=str, default='GA', help='SAR Algorithm : GA, GAKH, HYGAR')
    
    parser.add_argument('--clean_dep_rsf', action='store_true', help='Clean the dependency rsf file from self dependencies')

    # genetic algorithm args
    parser.add_argument('--max_iterations', type=int, default=100, help='Maximum iterations')
    parser.add_argument('--population_size', type=int, default=30, help='Population size')
    parser.add_argument('--crossover_probability', type=float, default=0.35, help='Crossover probability')
    parser.add_argument('--crossover_rate', type=float, default=0.5, help='Crossover rate')
    parser.add_argument('--mutation_probability', type=float, default=0.7, help='Mutation probability')
    parser.add_argument('--mutation_rate', type=float, default=0.06, help='Mutation rate')
    parser.add_argument('--elitism_probability', type=float, default=0.2, help='Elitism probability')
    parser.add_argument('--betas', type=float, default=0.0005, help='Roulette wheel ratio')
    parser.add_argument('--num_clusters', type=int, default=3, help='Number of clusters')
    parser.add_argument('--seed', type=int, default=519, help='Numpy random seed')
    parser.add_argument('--max_duration', type=int, default=10000, help='Maximum duration if the max number of iterations yet to be reached.')

    # metric
    parser.add_argument('--metric', type=str, default='directed_modularity', help='modularity, directed_modularity')

    # output
    parser.add_argument('--out_file', type=str, default='out.csv', help='output file')
    

    args = parser.parse_args()
    opt = vars(args)

    main(opt)
