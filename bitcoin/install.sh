cd ./bitcoin
vn="0.18.1"
fn="bitcoin-"${vn}"-x86_64-linux-gnu.tar.gz"
echo "Installing Bitcoin "${vn}" from "${fn}
curl -O https://bitcoin.org/bin/bitcoin-core-${vn}/${fn}
tar -xzvf ${fn} -C .
mv bitcoin-${vn} bitcoin
rm ${fn}
cd ..
sudo ln -s $PWD/bitcoin/bitcoin/bin/bitcoind /usr/local/bin/bitcoind
echo "Bitcoin installed"
