echo "rt restarting."
echo "killing rt"
ps aux | grep "python3 ./rt.py" | grep -v "grep" | awk '{print$2}' | xargs -r kill
echo "starting rt"
cd ./rt
nohup ./rt.py </dev/null >/dev/null 2>&1 &
cd ..
echo "rt started"
