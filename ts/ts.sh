echo "ts restarting."
echo "killing ts"
ps aux | grep "python3 ./ts.py" | grep -v "grep" | awk '{print$2}' | xargs -r kill
echo "starting ts"
cd ./ts
nohup ./ts.py &
#./ts.py
cd ..
echo "ts started"
