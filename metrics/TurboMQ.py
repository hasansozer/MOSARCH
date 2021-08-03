import sys
from RSFParser import *


if len(sys.argv) != 3:
	print("Usage:","python TurboMQ.py dependency.rsf clustering.rsf")
	exit(1)

parser = RSFParser(sys.argv[2])
parser.parse_dependency_input_file(sys.argv[1])
clustered_items = parser.clustered_items
count = len(clustered_items)

inter_cluster_dsm = [[0 for x in range(count)] for y in range(count)]
for x in range(count):
	elements1 = clustered_items[x]
	for y in range(x+1,count):
		elements2 = clustered_items[y]
		total = 0
		for e1 in elements1:
			for e2 in elements2:
				total += parser.dependency(e1, e2)
		
		inter_cluster_dsm[x][y] = inter_cluster_dsm[y][x] = total 

sum = 0.0
for i in range(count):
	elements = clustered_items[i]
	u = 0

	for e1 in range(len(elements)):
		for e2 in range(e1+1,len(elements)):
			u += parser.dependency(elements[e1], elements[e2])

	exdep = 0
	for j in range(count):
		exdep += inter_cluster_dsm[i][j]

	if(u == 0 and exdep == 0):
		continue
	
	cf = u / (u + 0.5 * exdep)
	if cf > 0:
		sum += cf

print(sum / count)