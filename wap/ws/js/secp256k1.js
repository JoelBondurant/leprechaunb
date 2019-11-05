/*
Leprechaun B, no rights reserved.
Secp256k1
*/


/*
secp256k1 group order.
*/
function ellipticOrder() {
	return 115792089237316195423570985008687907853269984665640564039457584007908834671663n;
}


/*
secp256k1 generator point order.
*/
function generatorOrder() {
	return 115792089237316195423570985008687907852837564279074904382605163141518161494337n;
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
Elliptic field addition.
*/
function ellipticAdd(a, b) {
	if (a == null) {
		return b;
	}
	if (b == null) {
		return a;
	}
	G = ellipticOrder();
	lam = ((b[1] - a[1]) * invMod(b[0] - a[0], G)) % G;
	x = (lam*lam - a[0]-b[0]) % G;
	y = (lam*(a[0] - x) - a[1]) % G;
	return [x, y];
}


/*
Elliptic point doubling.
*/
function ellipticDouble(a) {
	if (a == null) {
		return a;
	}
	G = ellipticOrder();
	lam = ((3n * a[0] * a[0]) * invMod(2n * a[1], G)) % G;
	x = (lam*lam - 2n*a[0]) % G;
	y = (lam*(a[0] - x) - a[1]) % G;
	return [x, y];
}


/*
Elliptic field scalar multiplication.
*/
function ellipticMultiply(b) {
	a = generatorPoint();
	c = null;
	for (i=0n; i<256n; i++) {
		if (b & (1n << i)) {
			c = ellipticAdd(c, a);
		}
		a = ellipticDouble(a);
	}
	return c;
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
	pubKey = ellipticMultiply(privKey);
	pubKey0 = pubKey[0].toString(16);
	pubKey1 = pubKey[1].toString(16);
	pubKey = [pubKey0, pubKey1];
	return pubKey;
}

