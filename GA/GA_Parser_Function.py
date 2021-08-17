import sys
import numpy as np
np.set_printoptions(threshold=sys.maxsize)

print("Usage python RSFParser.py bash-dependency.rsf bash-clustering.rsf")

def RSFParser(filename):
	RSFParser.filename = filename
	RSFParser.clustered_items = []
	RSFParser.name2ID = {}
	RSFParser.ID2name = {}
	RSFParser.total_item_count = 0
	ParseClusteringInputFile(RSFParser,filename)
	RSFParser.dsm = [[False for x in range(RSFParser.total_item_count)] for y in range(RSFParser.total_item_count)]

def dependency(parser,e1,e2):
	sum = 0
	if parser.dsm[parser.name2ID.get(e1)][parser.name2ID.get(e2)]: sum+=1
	if parser.dsm[parser.name2ID.get(e2)][parser.name2ID.get(e1)]: sum+=1
	return sum

def ParseClusteringInputFile(parser,filename):
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
		print("Error while reading an input file!111")

def parse_dependency_input_file(parser, filename):
	try:
		f = open(filename, "r+")
		
		for line in f:
			tokens = line.split()
			item_name = tokens[1]
			parser.dsm[parser.name2ID.get(item_name)][parser.name2ID.get(tokens[2])] = True

		f.close()

	except:
		print("Error while reading an input file!222")

RSFParser(sys.argv[2])
parse_dependency_input_file(RSFParser,sys.argv[1])
clustered_items = RSFParser.clustered_items

dsm_np = np.array([elem for row in RSFParser.dsm for elem in row])
