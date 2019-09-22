echo "Bitcoin Arrows starting."
git checkout v0.0.1
pkill python3
./rt/rt.sh
./ts/ts.sh
./arrows/arrows.sh
./wap/wap.sh
echo "Bitcoin Arrows started."
