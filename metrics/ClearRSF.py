import sys
import shutil
import hashlib
import os

try:
    filename = sys.argv[1]
    flags = sys.argv[2]
except:
    print("Usage: python ClearRSF.py filename flags \n" +
          "s : removes self dependencies \n" + 
          "u : removes duplicates \n")
    sys.exit(1)

if "s" in flags or "S" in flags:
    print("Clearing self dependencies")
    with open(filename, "r+") as f:
        with open("temp.txt", "w+") as f1:
            for line in f:
                tokens = line.rstrip().split()

                # remove self dependencies
                if tokens[1] == tokens[2]:
                    continue
                else:
                    f1.write(line)
    shutil.copyfile("temp.txt", filename)
    os.remove("temp.txt")

if "u" in flags or "U" in flags:

    shutil.copyfile(filename, filename + ".tmp")

    print("Clearing duplicate items")
    lines_hash = set()
    with open(filename + ".tmp", "r+") as f:
        with open(filename, "w+") as output_file:
            for line in f:
                hashValue = hashlib.md5(line.rstrip().encode('utf-8')).hexdigest()
                if hashValue not in lines_hash:
                    output_file.write(line)
                    lines_hash.add(hashValue)

    os.remove(filename + ".tmp")
