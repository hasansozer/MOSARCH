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
dependency_count = parser.dependency_count

print("number of clusters: ", cluster_count)
print("number of modules: ", module_count)
print("number of dependencies: ", dependency_count)

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

print((1 / dependency_count) * total)