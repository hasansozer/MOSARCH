def readfile(filename):
    ''' read the file and return the 3rd parameter in each line to an array then make the array unique'''
    arr = []
    with open(filename) as f:
        for line in f:
            arr.append(line.split()[2])
            arr.append(line.split()[1])
    return set(arr)


my_set = readfile('dataset/archstudio/archstudio-dependency.rsf')
print("archstudio : ",len(my_set))

my_set = readfile('dataset/bash/bash-dependency.rsf')
print("bash : ",len(my_set))

my_set = readfile('dataset/camel/camel-dependency.rsf')
print("camel : ",len(my_set))

my_set = readfile('dataset/chromium/chromium-dependency.rsf')
print("chromium : ",len(my_set))

my_set = readfile('dataset/cxf/cxf-dependency.rsf')
print("cxf : ",len(my_set))

my_set = readfile('dataset/hadoop/hadoop-dependency.rsf')
print("hadoop : ",len(my_set))

my_set = readfile('dataset/itk/itk-dependency.rsf')
print("itk : ",len(my_set))

my_set = readfile('dataset/lucene/lucene-3.6.0-deps.rsf')
print("lucene-3.6.0 : ",len(my_set))

my_set = readfile('dataset/lucene/lucene-4.6.1-deps.rsf')
print("lucene-4.6.1 : ",len(my_set))

my_set = readfile('dataset/nutch/nutch-2.3.1-deps.rsf')
print("nutch : ",len(my_set))

my_set = readfile('dataset/openjpa/openjpa-2.4.2-deps.rsf')
print("openjpa : ",len(my_set))

my_set = readfile('dataset/struts2/struts2-2.3.16-dependency.rsf')
print("struts2 : ",len(my_set))

my_set = readfile('dataset/wicket/wicket-dependency.rsf')
print("wicket : ",len(my_set))
