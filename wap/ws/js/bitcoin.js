/*
Leprechaun B, no rights reserved.
Bitcoin functions.
*/

var bitcoin = (function () {


/*
Get Bitcoin unspent output potential of an address.
*/
async function getAddressBalance(addr, confirmations=6) {
	base = 'https://blockchain.info/q/addressbalance/';
	resp = await fetch(base + addr + '?confirmations=' + confirmations);
	return resp.json();
}


/*
Bitcoin private keygen.
*/
function privateKey() {
	return secp256k1.privateKey();
}


/*
Bitcoin public keygen.
*/
async function publicKey(privKey, index=0, mainNet=true) {
	pubKey = secp256k1.publicKey(privKey, index);
	y = util.hexToBigInt(pubKey[1]);
	parity = (util.mod(y, 2n) == 0n);
	parityHex = '03';
	if (parity) {
		parityHex = '02';
	}
	pubKey = parityHex + pubKey[0]; // compressed key format;
	pubKey = util.bytesToHex(await util.sha256(util.hexToBytes(pubKey)));
	pubKey = CryptoJS.RIPEMD160(CryptoJS.enc.Hex.parse(pubKey)).toString()
	if (mainNet) {
		extendedRipemd = '00' + pubKey;
		pubKey = extendedRipemd;
	}
	pubKey = util.bytesToHex(await util.sha256(util.hexToBytes(pubKey)));
	pubKey = util.bytesToHex(await util.sha256(util.hexToBytes(pubKey)));
	chksum = pubKey.slice(0, 8);
	pubKey = extendedRipemd + chksum;
	pubKey = util.bytesToBase58(util.hexToBytes(pubKey));
	return pubKey;
}


/*
Bitcoin key pair.
*/
async function keyPair(index=0, mainNet=true) {
	k = privateKey();
	pk = await publicKey(k, index=index, mainNet=mainNet);
	return [k, pk];
}


return {
	privateKey: privateKey,
	publicKey: publicKey,
	keyPair: keyPair,
	getAddressBalance: getAddressBalance,
}


})();
