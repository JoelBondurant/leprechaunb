/*
Leprechaun B, no rights reserved.
Secp256k1 - dev wip.
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
	lam = (3n * a[0] * a[0]) * invMod(2n * a[1], G);
	x = mod(lam*lam - 2n*a[0], G);
	y = mod(lam*(a[0] - x) - a[1], G);
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
	lam = (y1 - y2) * invMod(x1 - x2, G);
	x = bigPow(lam, 2n) - (x1 + x2);
	y = lam * (x1 - x) - y1;
	return [mod(x, G), mod(y, G)];
}


/*
Elliptic scalar powers.
*/
function ellipticPower(a, k) {
	k = BigInt(k);
	if (k == 1n) {
		return a;
	}
	if (mod(k, 2n) == 1n) {
		return ellipticAdd(a, ellipticPower(a, k - 1n));
	}
	return ellipticPower(ellipticDouble(a), k / 2n);
}


/*
Format elliptic curve point as hex.
*/
function ellipticHex(a) {
	return a.map(x=>x.toString(16));
}


/*
Elliptic generator point powers.
*/
function generatorPower(k) {
	g = generatorPoint();
	return ellipticPower(g, k);
}


/*
Is point on secp256k1?
*/
function onCurve(a) {
	G = ellipticOrder();
	return (mod(a[1]*a[1] - a[0]*a[0]*a[0] - 7n, G) == 0n);
}


/*
secp256k1 private keygen.
*/
function privateKey() {
	k0 = crypto.getRandomValues(new Uint8Array(32));
	k = bytesToBigInt(k0);
	if (k > generatorOrder()) {
		return privateKey();
	}
	return k.toString(16);
}


/*
Secp256k1 public keygen.
*/
function publicKey(privKey, index=0) {
	pubKey = ellipticPower(privKey);
	return pubKey;
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
	onCurve: onCurve,
	privateKey: privateKey,
	publicKey: publicKey,
}


})();
