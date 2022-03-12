total_item_count = 0
dependency_count = 0
cluster_count = 0
clustered_items = []
name2ID = {}
dsm = []

def parse_directed_clustering_input_file(filename):
    global cluster_count
    global clustered_items
    global total_item_count
    global name2ID
    global dsm


    cluster_name = ""
    current_cluster = ""
    item_name = ""
    total_item_count = 0
    dependency_count = 0
    cluster_count = 0
    clustered_items = []
    name2ID = {}
    dsm = []

    f = open(filename, "r+")
    for line in f:
        tokens = line.split()
        cluster_name = tokens[1]
        if current_cluster != cluster_name:
            current_cluster = cluster_name
            cluster_count += 1
            clustered_items.append([])

        item_name = tokens[2]
        clustered_items[cluster_count - 1].append(item_name)
        name2ID.update({item_name: total_item_count})
        total_item_count += 1
    # for items in clustered_items:
    #     print(len(items))
    f.close()
    # exit()
    

def parse_directed_dependency_input_file(filename):
    global total_item_count
    global dependency_count
    global name2ID
    global dsm

    dependency_count = 0
    dsm = [[0 for i1 in range(total_item_count)] for i2 in range(total_item_count)]

    f = open(filename, "r+")
    
    for line in f:
        tokens = line.split()
        dsm[name2ID.get(tokens[1])][name2ID.get(tokens[2])] = 1
        dependency_count += 1
    f.close()


def modularity_directed(dependency_file, clustering_file):
    
    global total_item_count
    global dependency_count
    global name2ID
    global dsm

    parse_directed_clustering_input_file(clustering_file)
    parse_directed_dependency_input_file(dependency_file)
    

    d_out = [0 for index in range(total_item_count)]
    d_in = [0 for index in range(total_item_count)]
    for x in range(total_item_count):
        for y in range(total_item_count):
            d_out[x] += dsm[x][y]
            d_in[y] += dsm[x][y]

    total_sum = 0
    for c in range(cluster_count):
        modules = clustered_items[c]
        for e1 in range(len(modules)):
            for e2 in range(len(modules)):
                if e1 != e2:
                    total_sum += dsm[name2ID.get(modules[e1])][name2ID.get(modules[e2])]
                    total_sum -= (d_out[name2ID.get(modules[e1])] * d_in[name2ID.get(modules[e2])]) / dependency_count

    return cluster_count, total_item_count, dependency_count, (1 / dependency_count) * total_sum



from RSFParser import RSFParser

def modularity(dependency_file, clustering_file):
    parser = RSFParser(clustering_file)
    parser.parse_dependency_input_file(dependency_file)
    clustered_items = parser.clustered_items
    cluster_count = len(clustered_items)
    module_count = parser.total_item_count

    d = [0]*module_count
    for x in range(module_count):
        total = 0
        for y in range(x + 1, module_count):
            total += parser.dsm[x][y]
        d[x] = total

    total = 0
    for i in range(module_count):
        total += d[i]
    m = total/2

    total = 0
    for c in range(cluster_count):
        modules = clustered_items[c]
        for e1 in range(len(modules)):
            for e2 in range(e1+1,len(modules)):
                total += parser.dependency(modules[e1], modules[e2])
                total -= (d[e1]*d[e2])/(2*m)

    return cluster_count, module_count, 1/(2*m)*total


repos = {
          "archstudio" : ["archstudio-dependency.rsf", "archstudio-clustering.rsf"],
          "bash"       : ["bash-dependency.rsf", "bash-clustering.rsf"],
        #  "camel"      : ["camel-dependency.rsf"], # more memory is needed 16 GB is not enough
          "chromium"   : ["chromium-dependency.rsf", "chromium-clustering.rsf"],
        #  "cxf"        : ["cxf-dependency.rsf"], # more memory is needed 16 GB is not enough
          "hadoop"     : ["hadoop-dependency.rsf", "hadoop-clustering.rsf"],
          "itk"        : ["itk-dependency.rsf", "itk-clustering.rsf"],
        #  "lucene"     : ["lucene-4.6.1-deps.rsf"], # Type error
        #  "nutch"      : ["nutch-2.3.1-deps.rsf"], # Type error
        #  "openjpa"    : ["openjpa-2.4.2-deps.rsf"], # Type error
        #  "struts2"    : ["struts2-2.3.16-dependency.rsf"], # Type error
        #  "wicket"     : ["wicket-dependency.rsf"] # more memory is needed 16 GB is not enough
        }

mgmc_jar = "../experiments/clustering.jar"
rsf2txt  = "../experiments/rsf2txt.jar"
txt2rsf  = "../experiments/txt2rsf.jar"

import os
import csv

f = open("repo_information.csv", "w+", newline="")
writer = csv.writer(f)
writer.writerow(["Repository_Name", "Cluster_Count", "Total_Item_Count", "Modularity", "Directed_Modularity"])
f.close()

for repo in repos:
    print(repo + "/" + repos[repo][0])
    # convert dependency rsf to txt
    cmd = "java -jar " + rsf2txt + " ./" + repo + "/" + repos[repo][0] + " ./" + repo + "/" + "mgmc-clustered.txt"
    os.system(cmd)

    # use MGMC clustering algorithm to cluster the dependency graph
    cmd = "java -jar " + mgmc_jar + " " + repo + "/mgmc-clustered.txt" + " " + repo + "/output.txt"
    os.system(cmd)

    # convert the clustered dependency graph to rsf
    cmd = "java -jar " + txt2rsf + " " + repo + "/output.txt" + " " + repo + "/" + repo + "-mgmc-clustered.rsf"
    os.system(cmd)

    # remove temporary files
    os.remove(repo + "/mgmc-clustered.txt")
    os.remove(repo + "/output.txt")
 
    # use modularity algorithms to calculate the modularity of the clustered dependency graph
    path_dependency = "./" + repo + "/" + repos[repo][0]

    if len(repos[repo]) == 1:
        path_clustering = "./" + repo + "/" + repos[repo][0]    
    else:
        path_clustering = "./" + repo + "/" + repos[repo][1]

    directed_cluster_count, directed_total_item_count, dependency_count, directed_modularity = modularity_directed(path_dependency, path_clustering)
    cluster_count, total_item_count, modularity_ = modularity(path_dependency, path_clustering)

    print("Directed Cluster Count: " + str(directed_cluster_count))
    print("Directed Total Item Count: " + str(directed_total_item_count))
    print("Cluster Count: " + str(cluster_count))
    print("Total Item Count: " + str(total_item_count))
    print()
    print("Directed Modularity: " + str(directed_modularity))
    print("Modularity: " + str(modularity_))
    print("-------------------------------------------------------------")
    assert directed_cluster_count == cluster_count
    assert directed_total_item_count == total_item_count
    
    path_clustering = "./" + repo + "/" + repo + "-mgmc-clustered.rsf"
    mgmc_directed_cluster_count, mgmc_directed_total_item_count, mgmc_dependency_count, mgmc_directed_modularity = modularity_directed(path_dependency, path_clustering)
    mgmc_cluster_count, mgmc_total_item_count, mgmc_modularity_ = modularity(path_dependency, path_clustering)

    g = open("repo_information.csv", "a+", newline="")
    writer = csv.writer(g)
    writer.writerow([repo, cluster_count, total_item_count, dependency_count, modularity_, directed_modularity, mgmc_cluster_count, mgmc_total_item_count, mgmc_dependency_count, mgmc_modularity_, mgmc_directed_modularity])
    g.close()
