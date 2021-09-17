class RSFParser:

    def __init__(self, filename):
        self.filename = filename
        self.clustered_items = []
        self.name2ID = {}
        self.ID2name = {}
        self.total_item_count = 0

        # check if there is a clustering input file
        if "cxf" in filename or "camel" in filename:
            self.clear_self_dependencies(filename)
            self.get_filenames(filename)
        else:
            self.parse_clustering_input_file(filename)
        
        self.dsm = [[False for x in range(self.total_item_count)]
                    for y in range(self.total_item_count)]

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
            item_name = ""

            for line in f:
                tokens = line.split()
                item_name = tokens[2]
                
                self.name2ID.update({item_name: self.total_item_count})
                self.ID2name.update({self.total_item_count: item_name})
                self.total_item_count += 1

            f.close()
        except Exception as e:
            print(e)

    def clear_self_dependencies(self,filename):
        f = open(filename, "r+")
        a = []

        for line in f:
            tokens = line.split()
            item_name1 = tokens[1]
            item_name2 = tokens[2]

            # remove self dependencies
            if tokens[1] == tokens[2]:
                continue

            # check if the filename contains class dependencies
            if "$" in tokens[1]:
                item_name1 = tokens[1].split("$")[0]
            if "$" in tokens[2]:
                item_name2 = tokens[2].split("$")[0]

            arr = [tokens[0], item_name1, item_name2]

            # check if the item is already in the list
            if arr not in a:
                a.append(arr)

        f.close()
        file = open(filename, "w+")

        for line in a:
            str1 = "" 

            for ele in line: 
                str1 += ele
                str1 += " "

            str1 += "\n"
            file.write(str1)

        file.close()

    def get_filenames(self, filename):
        try:
            f = open(filename, "r+")
            item_name = ""

            for line in f:
                tokens = line.split()
                item_name1 = tokens[1]
                item_name2 = tokens[2]

                if item_name1 not in self.name2ID:
                    self.name2ID.update({item_name1: self.total_item_count})
                    self.ID2name.update({self.total_item_count: item_name1})
                    self.total_item_count += 1

                if item_name2 not in self.name2ID:
                    self.name2ID.update({item_name: self.total_item_count})
                    self.ID2name.update({self.total_item_count: item_name})
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
            f.close()
        except Exception as e:
            print(e)
