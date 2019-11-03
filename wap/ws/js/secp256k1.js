/*
Secp256k1
*/



/*
Big Square Root function.
*/
function bigSqrt(n) {
	m = BigInt(n);
	if (m < 0n) {
		throw "nope";
	}
	if (m < 2n) {
		return m;
	}
	function newtonIteration(n, x0) {
		const x1 = ((n / x0) + x0) >> 1n;
		if (x0 === x1 || x0 === (x1 - 1n)) {
			return x0;
		}
		return newtonIteration(n, x1);
	}
	return newtonIteration(m, 1n);
}


/*
Big Power function.
*/
function bigPow(a, b) {
	a = BigInt(a);
	b = BigInt(b);
	if (b == 0n) {
		return 1n;
	} else if ((b % 2n) == 1n) {
		return a*bigPow(a, b - 1n);
	} else {
		c = bigPow(a, b/2n);
		return c*c;
	}
}


/*
Big Absolute Value function.
*/
function bigAbs(x) {
	x = BigInt(x);
	if (x < 0n) {
		return -x;
	}
	return x;
}


/*
GCD function.
*/
function gcd(a, b) {
	a = bigAbs(a);
	b = bigAbs(b);
	if (b > a) {
		c = a;
		a = b;
		b = c;
	}
	while (true) {
		if (b == 0) {
			return a;
		}
		a %= b;
		if (a == 0) {
			return b;
		}
		b %= a;
	}
}


/*
Modular Inverse function.
*/
function invMod(a, b) {
	a = BigInt(a);
	b = BigInt(b);
	if (a == 0n) {
		return 0n;
	} else if ((b % a) == 0n) {
		return 1n;
	} else {
		return b - invMod(b % a, a) * b / a;
	}
}


/*
secp256k1 group order.
*/
function ellipticOrder() {
	return 115792089237316195423570985008687907853269984665640564039457584007908834671663n;
}


/*
secp256k1 generator.
*/
function ellipticGenerator() {
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
	a = ellipticGenerator();
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
Secp256k1 public key gen.
*/
function ellipticKey(privKey) {
	pubKey = ellipticMultiply(privKey);
	pubKey0 = Array.from(hexToUint8Array(pubKey[0].toString(16)));
	pubKey1 = Array.from(hexToUint8Array(pubKey[1].toString(16)));
	pubKey = pubKey0.concat(pubKey1);
	return uint8ArrayToHex(pubKey);
}
