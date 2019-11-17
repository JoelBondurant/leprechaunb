/*
Leprechaun B, no rights reserved.
Bitcoin - dev wip.
*/

var bitcoin = (function () {

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
	pubKey = await util.sha256(util.hexToBytes(pubKey));
	return util.bytesToHex(pubKey);
}


return {
	privateKey: privateKey,
	publicKey: publicKey,
}


})();
