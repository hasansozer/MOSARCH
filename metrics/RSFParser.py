class RSFParser:

	def dependency(self, e1, e2):
		sum = 0
		if self.dsm[self.name2ID.get(e1)][self.name2ID.get(e2)]: sum+=1
		if self.dsm[self.name2ID.get(e2)][self.name2ID.get(e1)]: sum+=1
		return sum


	def __init__(self, filename):
		self.filename = filename
		self.clustered_items = []
		self.name2ID = {}
		self.total_item_count = 0

		self.parse_clustering_input_file(filename)
		self.dsm = [[False for x in range(self.total_item_count)] for y in range(self.total_item_count)]


	def parse_clustering_input_file(self, filename):
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
					self.clustered_items.append([])	 
				

				item_name = tokens[2]
				self.clustered_items[cluster_count-1].append(item_name)
				self.name2ID.update({item_name: self.total_item_count})
				self.total_item_count += 1

			f.close()
		except Exception as e:
			print(e)


	def parse_dependency_input_file(self, filename):
			f = open(filename, "r+")
			a = []

			for line in f:
				tokens = line.split()
				a.append(tokens)
				item_name = tokens[1]
				try:
					self.dsm[self.name2ID.get(item_name)][self.name2ID.get(tokens[2])] = True
				except:
					a.pop()

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
