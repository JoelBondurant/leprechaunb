/*
Leprechaun B, no rights reserved.
Secp256k1 based on javascript BigInt.
*/

var secp256k1 = (function () {

/*
secp256k1 group order of the elliptic addition.
*/
function ellipticOrder() {
	return 115792089237316195423570985008687907853269984665640564039457584007908834671663n;
}


/*
secp256k1 generator point.
*/
function generatorPoint() {
	x = 55066263022277343669578718895168534326250603453777594175500187360389116729240n;
	y = 32670510020758816978083085130507043184471273380659243275938904335757337482424n;
	return [x, y];
}


/*
secp256k1 cyclic group order of additive powers of the generator point.
G*1, G*2, ...G*n ~ Zn
*/
function generatorOrder() {
	return 115792089237316195423570985008687907852837564279074904382605163141518161494337n;
}


/*
The elliptic identity.
*/
function ellipticIdentity() {
	return null;
}


/*
Is this the elliptic identity.
*/
function isEllipticIdentity(a) {
	return (a == null);
}


/*
Elliptic additive inverse.
*/
function ellipticInverse(a) {
	if (isEllipticIdentity(a)) {
		return ellipticIdentity();
	}
	return [a[0], -a[1]];
}


/*
Elliptic point doubling.
*/
function ellipticDouble(a) {
	if (isEllipticIdentity(a)) {
		return ellipticIdentity();
	}
	if (a[1] == 0n) {
		return ellipticIdentity();
	}
	G = ellipticOrder();
	lam = (3n * a[0] ** 2n) * util.invMod(2n * a[1], G);
	x = util.mod(lam**2n - 2n*a[0], G);
	y = util.mod(lam*(a[0] - x) - a[1], G);
	return [x, y];
}


/*
Elliptic addition.
*/
function ellipticAdd(a, b) {
	if (isEllipticIdentity(a)) {
		return b;
	}
	if (isEllipticIdentity(b)) {
		return a;
	}
	if (a == b) {
		return ellipticDouble(a);
	}
	G = ellipticOrder();
	[x1, y1] = a;
	[x2, y2] = b;
	lam = (y1 - y2) * util.invMod(x1 - x2, G);
	x = (lam**2n) - (x1 + x2);
	y = lam * (x1 - x) - y1;
	return [util.mod(x, G), util.mod(y, G)];
}


/*
Elliptic scalar powers.
*/
function ellipticPower(a, k) {
	k = BigInt(k);
	if (k == 1n) {
		return a;
	}
	if (util.mod(k, 2n) == 1n) {
		return ellipticAdd(a, ellipticPower(a, k - 1n));
	}
	return ellipticPower(ellipticDouble(a), k / 2n);
}


/*
Format elliptic curve point as hex.
*/
function ellipticHex(a) {
	if (isEllipticIdentity(a)) {
		return ['0','0'];
	}
	return a.map(x=>x.toString(16));
}


/*
Elliptic generator point powers.
*/
function generatorPower(k) {
	if (typeof(k) == 'string') {
		k = util.hexToBigInt(k);
	}
	if (k <= 0n) {
		return ellipticIdentity();
	}
	g = generatorPoint();
	return ellipticPower(g, k);
}


/*
Is point on secp256k1?
*/
function isOnCurve(a) {
	G = ellipticOrder();
	return (util.mod(a[1]**2n - a[0]**3n - 7n, G) == 0n);
}


/*
secp256k1 private keygen.
*/
function privateKey() {
	k0 = crypto.getRandomValues(new Uint8Array(32));
	k = util.bytesToBigInt(k0);
	if (k > generatorOrder()) {
		return privateKey();
	}
	return k.toString(16);
}


/*
Secp256k1 public keygen.
*/
function publicKey(privKey, index=0) {
	if (typeof(privKey) == 'string') {
		privKey = util.hexToBigInt(privKey);
	}
	pubKey = generatorPower(privKey);
	return ellipticHex(pubKey);
}


return {
	ellipticOrder: ellipticOrder,
	generatorPoint: generatorPoint,
	generatorOrder: generatorOrder,
	ellipticIdentity: ellipticIdentity,
	isEllipticIdentity: isEllipticIdentity,
	ellipticInverse: ellipticInverse,
	ellipticDouble: ellipticDouble,
	ellipticAdd: ellipticPower,
	ellipticHex: ellipticHex,
	generatorPower: generatorPower,
	isOnCurve: isOnCurve,
	privateKey: privateKey,
	publicKey: publicKey,
}


})();
