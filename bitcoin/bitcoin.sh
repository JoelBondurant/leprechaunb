# bitcoin-core.cli -getinfo
# bitcoin-core.cli getblockchaininfo
echo "Bitcoin starting..."
echo "Killing Bitcoin."
kill -9 $(pgrep bitcoin)
sleep 4
echo "Startup..."
pwd0=$PWD
cd ~
nohup nice bitcoin-core.daemon -daemon -prune=100000 -listen=0 -blocksonly=1 -dbcache=10 -maxorphantx=10 -maxmempool=10 -maxconnections=4 -maxsigcachesize=2 -rpcthreads=1 -par=1 </dev/null >/dev/null 2>&1 &
cd $pwd0
echo "Bitcoin started."
