deps="archstudio bash hadoop lucene nutch openjpa struts2"

for file in $deps
do
    filename="${file}-dependency.rsf"
    echo $filename
    python MainGAMGMC.py $filename &
done

wait

for file in $deps
do
    mkdir -p "${file}_results"
    mv *${file}*.csv "${file}_results/"
done
