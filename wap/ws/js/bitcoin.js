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
async function publicKey(privKey, index=0) {
	pubKey = secp256k1.publicKey(privKey, index);
	pubKey = '02' + pubKey[0];
	pubKey = util.bytesToHex(await util.sha256(util.hexToBytes(pubKey)));
	pubKey = CryptoJS.RIPEMD160(CryptoJS.enc.Hex.parse(pubKey)).toString()
	return pubKey;
}


return {
	privateKey: privateKey,
	publicKey: publicKey,
}


})();
