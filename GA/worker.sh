deps="bash"

for file in $deps
do
    filename="${file}-dependency.rsf"
    echo $filename
    python Main.py $filename
done


for file in $deps
do
    mkdir -p "${file}_results"
    mv *${file}*.csv "${file}_results/"
done
