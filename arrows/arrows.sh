echo "arrows restarting."
echo "killing arrows"
ps aux | grep "python3 ./arrows.py" | grep -v "grep" | awk '{print$2}' | xargs -r kill
echo "starting arrows"
cd ./arrows
nohup ./arrows.py &
#./arrows.py
cd ..
echo "arrows done"
