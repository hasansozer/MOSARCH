#!/bin/bash

rsf_files="bash-dependency.rsf archstudio-dependency.rsf hadoop-dependency.rsf lucene-4.6.1-deps.rsf openjpa-2.4.2-deps.rsf"

for project in $rsf_files
do
    java -jar ../rsf2txt.jar ../${project} "dep_${project}.txt"
    java -jar ../clustering.jar "dep_${project}.txt" "clustered_${project}.txt"
    java -jar ../txt2rsf.jar "clustered_${project}.txt" "clustered_${project}"
    rm "dep_${project}.txt"
    rm "clustered_${project}.txt"
done
