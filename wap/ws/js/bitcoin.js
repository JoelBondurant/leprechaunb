/*
Leprechaun B, no rights reserved.
Bitcoin functions.
*/

var bitcoin = (function () {


/*
Get Bitcoin unspent output potential of an address.
*/
async function getAddressBalance(addr, confirmations=6) {
	var base = 'https://blockchain.info/q/addressbalance/';
	var resp = await fetch(base + addr + '?confirmations=' + confirmations);
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
	var pubKey = secp256k1.publicKey(privKey, index);
	var y = util.hexToBigInt(pubKey[1]);
	var parity = (util.mod(y, 2n) == 0n);
	var parityHex = '03';
	if (parity) {
		parityHex = '02';
	}
	var pubKey = parityHex + pubKey[0]; // compressed key format;
	pubKey = util.bytesToHex(await util.sha256(util.hexToBytes(pubKey)));
	pubKey = CryptoJS.RIPEMD160(CryptoJS.enc.Hex.parse(pubKey)).toString()
	if (mainNet) {
		var extendedRipemd = '00' + pubKey;
		pubKey = extendedRipemd;
	}
	pubKey = util.bytesToHex(await util.sha256(util.hexToBytes(pubKey)));
	pubKey = util.bytesToHex(await util.sha256(util.hexToBytes(pubKey)));
	var chksum = pubKey.slice(0, 8);
	pubKey = extendedRipemd + chksum;
	pubKey = util.bytesToBase58(util.hexToBytes(pubKey));
	return pubKey;
}


/*
Bitcoin key pair.
*/
async function keyPair(index=0, mainNet=true) {
	var k = privateKey();
	var pk = await publicKey(k, index=index, mainNet=mainNet);
	return [k, pk];
}


/*
Bitcoin signature.
*/
async function sign(msg, privKey) {
	var hexMsg = util.bytesToHex(await util.sha256(msg));
	var signature = secp256k1.sign(hexMsg, privKey);
	return signature;
}


/*
Bitcoin signature verification.
*/
async function verify(msg, signature, pubKey) {
	var hexMsg = util.bytesToHex(await util.sha256(msg));
	return secp256k1.verify(hexMsg, signature, pubKey);
}


return {
	privateKey: privateKey,
	publicKey: publicKey,
	keyPair: keyPair,
	getAddressBalance: getAddressBalance,
	sign: sign,
	verify: verify,
}


})();
