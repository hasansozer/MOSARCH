class RSFParser:
    def __init__(self):
        self.clustered_items = []
        self.cluster_names = {}
        self.name2ID = {}
        self.ID2name = {}
        self.total_item_count = 0
        self.dependency_count = 0
        self.dsm = []
        self.d_in = []
        self.d_out = []


    def dependency(self, e1, e2):
        sum = 0
        if self.dsm[self.name2ID.get(e1)][self.name2ID.get(e2)]:
            sum += 1
        if self.dsm[self.name2ID.get(e2)][self.name2ID.get(e1)]:
            sum += 1
        return sum


    def parse_dependency_input_file(self, dependency_file):
        try:
            with open(dependency_file, "r+") as f:
                for line in f:
                    tokens = line.strip().split()
                    item_name1 = tokens[1]
                    item_name2 = tokens[2]

                    if item_name1 not in self.name2ID:
                        self.name2ID.update({item_name1: self.total_item_count})
                        self.ID2name.update({self.total_item_count: item_name1})
                        self.total_item_count += 1

                    if item_name2 not in self.name2ID:
                        self.name2ID.update({item_name2: self.total_item_count})
                        self.ID2name.update({self.total_item_count: item_name2})
                        self.total_item_count += 1

                    self.dependency_count += 1

            self.dsm   = [[False for _ in range(self.total_item_count)] for _ in range(self.total_item_count)]
            self.d_in  = [0]*self.total_item_count
            self.d_out = [0]*self.total_item_count


            with open(dependency_file, "r+") as f:
                for line in f:
                    tokens = line.strip().split()
                    item_name1 = tokens[1]
                    item_name2 = tokens[2]
                    self.dsm[self.name2ID.get(item_name1)][self.name2ID.get(item_name2)] = True
                    self.d_in[self.name2ID.get(item_name2)] += 1
                    self.d_out[self.name2ID.get(item_name1)] += 1

        except Exception as e:
            print(e)


    def parse_clustering_input_file(self, clustering_file):
        try:
            self.clustered_items = []
            self.cluster_names = {}
            with open(clustering_file, "r+") as f:
                for line in f:
                    tokens = line.strip().split()
                    cluster_name = tokens[1]
                    item_name    = tokens[2]

                    if cluster_name not in self.cluster_names:
                        self.cluster_names.update({cluster_name: cluster_index})
                        self.clustered_items.append([])
                        self.clustered_items[cluster_index].append(item_name)
                        cluster_index += 1
                    else:
                        temp_index = self.cluster_names.get(cluster_name)
                        self.clustered_items[temp_index].append(item_name)

        except Exception as e:
            print(e)


    def get_jaya_random_list(self, clustering_file):
        bias = 0.0001
        jaya_initial_list = []
        with open(clustering_file, "r+") as f:
            for line in f:
                tokens = line.split()
                cluster = tokens[1]
                cluster_index = self.cluster_names[cluster]
                
                import random
                random_number = random.uniform(cluster_index / self.total_item_count + bias, (cluster_index+1)/self.total_item_count - bias)
                jaya_initial_list.append(random_number)

        for i in range(len(self.clustered_items)):
            jaya_initial_list.append((i+1) / self.total_item_count)

        return jaya_initial_list

    def get_genetic_list(self, clustering_file):
        genetic_list = []
        with open(clustering_file, "r+") as f:
            for line in f:
                tokens = line.split()
                cluster = tokens[1]
                cluster_index = self.cluster_names[cluster]
                genetic_list.append(cluster_index)
        return genetic_list
