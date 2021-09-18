import sys
import numpy as np
def write_to_file(file_name, content):
    file = open(filename, "w+")

    for line in a:
        str1 = "" 

        for ele in line: 
            str1 += ele
            str1 += " "

        str1 += "\n"
        file.write(str1)

    file.close()

try:
    filename = sys.argv[1]
    flags = sys.argv[2]
except:
    print("Usage: python ClearRSF.py flags \n" +
          "c : removes $ from filenames \n" + 
          "s : removes self dependencies \n" + 
          "u : removes duplicates \n")
    sys.exit(1)

if "c" in flags or "C" in flags:
    print("Clearing special characters")
    f = open(filename, "r+")
    a = []
    for line in f:
        tokens = line.split()
        item_name1 = tokens[1]
        item_name2 = tokens[2]

        if "$" in tokens[1]:
            item_name1 = tokens[1].split("$")[0]
        if "$" in tokens[2]:
            item_name2 = tokens[2].split("$")[0]

        arr = [tokens[0], item_name1, item_name2]
        a.append(arr)

    f.close()
    write_to_file(filename, a)


if "s" in flags or "S" in flags:
    print("Clearing self dependencies")
    a = []
    f = open(filename, "r+")
    for line in f:
        tokens = line.split()
        item_name1 = tokens[1]
        item_name2 = tokens[2]

        # remove self dependencies
        if tokens[1] == tokens[2]:
            continue

        arr = [tokens[0], item_name1, item_name2]
        a.append(arr)
    f.close()
    write_to_file(filename, a)
        

if "u" in flags or "U" in flags:
    print("Clearing duplicate items")
    f = open(filename, "r+")
    a = []
    for line in f:
        tokens = line.split()
        item_name1 = tokens[1]
        item_name2 = tokens[2]

        arr = [tokens[0], item_name1, item_name2]

        a.append(arr)
    
    f.close()
    b = np.array(a)
    c = np.unique(b, axis=0)
    write_to_file(filename, c)