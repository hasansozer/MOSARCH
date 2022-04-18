class RSFParser:

    def __init__(self, filename):
        self.filename = filename
        self.clustered_items = []
        self.name2ID = {}
        self.ID2name = {}
        self.total_item_count = 0
        self.dependency_count = 0

        # check if there is a clustering input file
        if "deps" in filename or "dependency" in filename:
            self.get_filenames(filename)
        else:
            self.parse_clustering_input_file(filename)
        
        self.dsm = [[False for x in range(self.total_item_count)] for y in range(self.total_item_count)]

    def dependency(self, e1, e2):
        sum = 0
        if self.dsm[self.name2ID.get(e1)][self.name2ID.get(e2)]:
            sum += 1
        if self.dsm[self.name2ID.get(e2)][self.name2ID.get(e1)]:
            sum += 1
        return sum

    def parse_clustering_input_file(self, filename):
        try:
            f = open(filename, "r+")
            cluster_names = {}
            cluster_index = 0
            
            for line in f:
                tokens = line.split()
                cluster_name = tokens[1]
                item_name = tokens[2]

                if cluster_name not in cluster_names:
                    cluster_names.update({cluster_name: cluster_index})
                    self.clustered_items.append([])
                    self.clustered_items[cluster_index].append(item_name)
                    cluster_index += 1
                else:
                    temp_index = cluster_names.get(cluster_name)
                    self.clustered_items[temp_index].append(item_name)

                self.name2ID.update({item_name: self.total_item_count})
                self.ID2name.update({self.total_item_count: item_name})
                self.total_item_count += 1

            f.close()
        except Exception as e:
            print(e)

    def get_filenames(self, filename):
        try:
            f = open(filename, "r+")

            for line in f:
                tokens = line.split()
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

            f.close()
        except Exception as e:
            print(e)


    def parse_dependency_input_file(self, filename):
        try:
            f = open(filename, "r+")

            for line in f:
                tokens = line.split()
                item_name = tokens[1]
                self.dsm[self.name2ID.get(item_name)][self.name2ID.get(tokens[2])] = True
                self.dependency_count += 1
            f.close()
        except Exception as e:
            print(e)
