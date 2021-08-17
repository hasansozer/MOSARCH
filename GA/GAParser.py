import sys
import numpy as np
#np.set_printoptions(threshold=sys.maxsize)

#print("Usage python GAParser.py bash-dependency.rsf bash-clustering.rsf")

def GAParser(dependency, clustering):
	GAParser.dependency = dependency
	GAParser.clustering = clustering
	GAParser.clustered_items = []
	GAParser.name2ID = {}
	GAParser.ID2name = {}
	GAParser.total_item_count = 0
	parse_clustering_input_file(GAParser, GAParser.clustering)
	GAParser.dsm = [[False for x in range(GAParser.total_item_count)] for y in range(GAParser.total_item_count)]
	parse_dependency_input_file(GAParser, GAParser.dependency)
	dsm_np = np.array([elem for row in GAParser.dsm for elem in row])
	
	return(dsm_np,GAParser.ID2name, GAParser.clustered_items)

def dependency(parser,e1,e2):
	sum = 0
	if parser.dsm[parser.name2ID.get(e1)][parser.name2ID.get(e2)]: sum+=1
	if parser.dsm[parser.name2ID.get(e2)][parser.name2ID.get(e1)]: sum+=1
	return sum

def parse_clustering_input_file(parser,filename):
	try:
		f = open(filename, "r+")
		cluster_name = ""
		current_cluster = ""
		item_name = ""
		cluster_count = 0
		
		for line in f:
			tokens = line.split()
			cluster_name = tokens[1]
			if current_cluster != cluster_name:
				current_cluster = cluster_name
				cluster_count += 1
				parser.clustered_items.append([])	 
			

			item_name = tokens[2]
			parser.clustered_items[cluster_count-1].append(item_name)
			parser.ID2name.update({parser.total_item_count: item_name })
			parser.name2ID.update({item_name: parser.total_item_count })
			parser.total_item_count += 1
		f.close()
	except:
		print("Error while reading clustering input file!")

def parse_dependency_input_file(parser, filename):
	try:
		f = open(filename, "r+")
		
		for line in f:
			tokens = line.split()
			item_name = tokens[1]
			parser.dsm[parser.name2ID.get(item_name)][parser.name2ID.get(tokens[2])] = True

		f.close()

	except:
		print("Error while reading the dependency input file!")
