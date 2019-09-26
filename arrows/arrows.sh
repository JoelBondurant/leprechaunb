echo "arrows restarting."
echo "killing arrows"
ps aux | grep "python3 ./arrows.py" | grep -v "grep" | awk '{print$2}' | xargs -r kill
echo "starting arrows"
cd ./arrows
nohup ./arrows.py </dev/null >/dev/null 2>&1 &
cd ..
echo "arrows done"
