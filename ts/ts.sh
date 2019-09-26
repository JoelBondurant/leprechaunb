echo "ts restarting."
echo "killing ts"
ps aux | grep "python3 ./ts.py" | grep -v "grep" | awk '{print$2}' | xargs -r kill
echo "starting ts"
cd ./ts
nohup ./ts.py </dev/null >/dev/null 2>&1 &
cd ..
echo "ts started"
