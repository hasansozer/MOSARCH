deps="chromium"

for file in $deps
do
    filename="${file}-dependency.rsf"
    echo $filename
    python average_runs.py $filename &
done

wait

mkdir -p ./average_runs
mv *HYGARIII.csv ./average_runs
