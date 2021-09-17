import sys

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


filename = sys.argv[1]
flags = sys.argv[2]

print("Clearing self dependencies")


if "s" in flags or "S" in flags:
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
        
if "c" in flags or "C" in flags:
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

if "u" in flags or "U" in flags:
    f = open(filename, "r+")
    a = []
    for line in f:
        tokens = line.split()
        item_name1 = tokens[1]
        item_name2 = tokens[2]

        arr = [tokens[0], item_name1, item_name2]

        if arr not in a:
            a.append(arr)
    
    f.close()
    write_to_file(filename, a)
