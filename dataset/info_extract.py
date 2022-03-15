import shutil
import hashlib
from RSFParser import RSFParser

def modularity_directed(dependency_file, clustering_file):

	parser = RSFParser(clustering_file)
	parser.parse_dependency_input_file(dependency_file)
	clustered_items = parser.clustered_items
	cluster_count = len(clustered_items)
	module_count = parser.total_item_count
	dependency_count = parser.dependency_count

	d = [0]*module_count
	d_out = [0 for index in range(module_count)]
	d_in = [0 for index in range(module_count)]

	for x in range(module_count):
		for y in range(module_count):
			d_out[x] += parser.dsm[x][y]
			d_in[y] += parser.dsm[x][y]

	total = 0
	for c in range(cluster_count):
		modules = clustered_items[c]
		for e1 in range(len(modules)):
			for e2 in range(len(modules)):
				if e1 != e2:
					total += parser.dsm[parser.name2ID.get(modules[e1])][parser.name2ID.get(modules[e2])]
					total -= (d_out[parser.name2ID.get(modules[e1])] * d_in[parser.name2ID.get(modules[e2])]) / dependency_count

	return cluster_count, module_count, dependency_count, (1 / dependency_count) * total




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


def clear_dependency_file(filename):
	print("Converting class dependencies to module dependencies")
	shutil.copyfile(filename, filename + ".tmp")
	f = open(filename + ".tmp", "r")
	g = open(filename, "w+")

	for line in f:
		tokens = line.split()
		g.write(tokens[0] + " " + tokens[1].split("$")[0] + " " + tokens[2].split("$")[0] + "\n")

	f.close()
	g.close()

	print("Clearing self dependencies")
	with open(filename, "r+") as f:
		with open("temp.txt", "w+") as f1:
			for line in f:
				tokens = line.rstrip().split()

				# remove self dependencies
				if tokens[1] == tokens[2]:
					continue
				else:
					f1.write(line)
	shutil.copyfile("temp.txt", filename)
	os.remove("temp.txt")

	shutil.copyfile(filename, filename + ".tmp")

	print("Clearing duplicate items")
	lines_hash = set()
	with open(filename + ".tmp", "r+") as f:
		with open(filename, "w+") as output_file:
			for line in f:
				hashValue = hashlib.md5(line.rstrip().encode('utf-8')).hexdigest()
				if hashValue not in lines_hash:
					output_file.write(line)
					lines_hash.add(hashValue)

	os.remove(filename + ".tmp")


repos = {
			"archstudio" : ["archstudio-dependency.rsf", "archstudio-clustering.rsf"],
			"bash"       : ["bash-dependency.rsf", "bash-clustering.rsf"],
			# "camel"      : ["camel-dependency.rsf"], # more memory is needed 16 GB is not enough
			"chromium"   : ["chromium-dependency.rsf", "chromium-clustering.rsf"],
			# "cxf"        : ["cxf-dependency.rsf"], # more memory is needed 16 GB is not enough
			"hadoop"     : ["hadoop-dependency.rsf", "hadoop-clustering.rsf"],
			"itk"        : ["itk-dependency.rsf", "itk-clustering.rsf"],
			"lucene"     : ["lucene-4.6.1-deps.rsf"],
			"nutch"      : ["nutch-2.3.1-deps.rsf"],
			"openjpa"    : ["openjpa-2.4.2-deps.rsf"],
			"struts2"    : ["struts2-2.3.16-dependency.rsf"],
			# "wicket"     : ["wicket-dependency.rsf"] # more memory is needed 16 GB is not enough
		}

mgmc_jar = "../experiments/clustering.jar"
rsf2txt  = "../experiments/rsf2txt.jar"
txt2rsf  = "../experiments/txt2rsf.jar"

import os
import csv

f = open("repo_information.csv", "w+", newline="")
writer = csv.writer(f)
writer.writerow(["Repository_Name", "Has_Clustering_File", "Cluster_Count", "Total_Item_Count", "Dependency_Count", "Modularity", "Directed_Modularity", "MGMC_Cluster_Count", "MGMC_Total_Item_Count", "MGMC_Dependency_Count", "MGMC_Modularity", "MGMC_Directed_Modularity"])
f.close()

for repo in repos:
	print("\nProcessing " + repo)
	clear_dependency_file("./" + repo + "/" + repos[repo][0])

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

for repo in repos:
	# use modularity algorithms to calculate the modularity of the clustered dependency graph
	path_dependency = "./" + repo + "/" + repos[repo][0]

	has_clustering = False
	if len(repos[repo]) == 1:
		path_clustering = "./" + repo + "/" + repos[repo][0]    
	else:
		has_clustering = True
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

	assert mgmc_directed_cluster_count == mgmc_cluster_count
	assert mgmc_directed_total_item_count == mgmc_total_item_count

	g = open("repo_information.csv", "a+", newline="")
	writer = csv.writer(g)
	writer.writerow([repo, str(has_clustering), cluster_count, total_item_count, dependency_count, modularity_, directed_modularity, mgmc_cluster_count, mgmc_total_item_count, mgmc_dependency_count, mgmc_modularity_, mgmc_directed_modularity])
	g.close()
