import sys

total_item_count = 0
dependency_count = 0
cluster_count = 0
clustered_items = []
name2ID = {}
dsm = []


def parse_clustering_input_file(filename):
    global cluster_count
    global clustered_items
    global total_item_count
    global name2ID
    global dsm

    f = open(filename, "r+")
    cluster_name = ""
    current_cluster = ""
    item_name = ""

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

    f.close()

    dsm = [[0 for i1 in range(total_item_count)] for i2 in range(total_item_count)]


def parse_dependency_input_file(filename):
    global total_item_count
    global dependency_count
    global name2ID
    global dsm

    f = open(filename, "r+")

    for line in f:
        tokens = line.split()
        dsm[name2ID.get(tokens[1])][name2ID.get(tokens[2])] = 1
        dependency_count += 1
    f.close()


def modularity():
    global total_item_count
    global dependency_count
    global name2ID
    global dsm

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

    return (1 / dependency_count) * total_sum


if __name__ == '__main__':

    if len(sys.argv) != 3:
        print("Usage:", "python modularity-directed.py dependency.rsf clustering.rsf")
        exit(1)

    parse_clustering_input_file(sys.argv[2])
    parse_dependency_input_file(sys.argv[1])

    print("number of clusters: ", cluster_count)
    print("number of modules: ", total_item_count)
    print("number of dependencies: ", dependency_count)
    print("directed modularity: ", modularity())
