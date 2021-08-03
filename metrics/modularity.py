import sys
from RSFParser import *

if len(sys.argv) != 3:
    print("Usage:", "python modularity.py dependency.rsf clustering.rsf")
    exit(1)

parser = RSFParser(sys.argv[2])
parser.parse_dependency_input_file(sys.argv[1])
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

print(1/(2*m)*total)
