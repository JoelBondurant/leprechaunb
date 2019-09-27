# bitcoin-core.cli getblockchaininfo
echo "Bitcoin starting..."
echo "Killing Bitcoin."
kill -9 $(pgrep bitcoin)
sleep 4
echo "Startup..."
nohup nice bitcoin-core.daemon -daemon -prune=550 -listen=0 -blocksonly=1 -dbcache=10 -maxorphantx=10 -maxmempool=10 -maxconnections=4 -maxsigcachesize=2 -rpcthreads=1 -par=1 </dev/null >/dev/null 2>&1 &
sleep 4
echo "CPU limiting..."
cpulimit --pid=$(pgrep bitcoin) --limit=80 --background
echo "Bitcoin started."
