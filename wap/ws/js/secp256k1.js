/*
Leprechaun B, no rights reserved.
Secp256k1 - dev wip.
*/


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
secp256k1 cyclic group order of elliptic scalar multiplication or the generator point.
G*1, G*2, ...G*n ~ Zn
G * 5 = G + G + G + G + G = (G * 2) * 2 + G
*/
function generatorOrder() {
	return 115792089237316195423570985008687907852837564279074904382605163141518161494337n;
}


/*
Elliptic point doubling.
*/
function ellipticDouble(a) {
	if (a == null) {
		return null;
	}
	if (a[1] == 0n) {
		return null;
	}
	G = ellipticOrder();
	lam = ((3n * a[0] * a[0]) * invMod(2n * a[1], G));
	x = (lam*lam - 2n*a[0]) % G;
	y = (lam*(a[0] - x) - a[1]) % G;
	if (y < 0n) {
		y = y + G;
	}
	return [x, y];
}


/*
Elliptic addition.
*/
function ellipticAdd(a, b) {
	if (a == null) {
		return b;
	}
	if (b == null) {
		return a;
	}
	if (a == b) {
		return ellipticDouble(a);
	}
	G = ellipticOrder();
	lam = ((b[1] - a[1]) * invMod(b[0] - a[0], G)) % G;
	x = (lam*lam - a[0] - b[0]) % G;
	y = (lam*(a[0] - x) - a[1]) % G;
	return [x, y];
}


/*
Elliptic scalar multiplication.
*/
function ellipticMultiply(b) {
	a = generatorPoint();
	bbin = b.toString(2);
	c = a;
	for (i=0; i<256; i++) {
		if (bbin[i] == null) {
			break;
		}
		if (bbin[i] == "1") {
			c = ellipticAdd(c, a);
		}
		a = ellipticDouble(a);
	}
	return c;
}


/*
Is point on secp256k1?
*/
function onCurve(a) {
	G = ellipticOrder();
	return (((a[1]*a[1] - a[0]*a[0]*a[0] - 7n) % G) == 0n);
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
	return pubKey;
}

