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
	var x = 55066263022277343669578718895168534326250603453777594175500187360389116729240n;
	var y = 32670510020758816978083085130507043184471273380659243275938904335757337482424n;
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
	var G = ellipticOrder();
	var lam = (3n * a[0] ** 2n) * util.invMod(2n * a[1], G);
	var x = util.mod(lam**2n - 2n*a[0], G);
	var y = util.mod(lam*(a[0] - x) - a[1], G);
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
	var G = ellipticOrder();
	[x1, y1] = a;
	[x2, y2] = b;
	var lam = (y1 - y2) * util.invMod(x1 - x2, G);
	var x = (lam**2n) - (x1 + x2);
	var y = lam * (x1 - x) - y1;
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
Zero pad hex strings to length 64 by default.
*/
function zeroPad(hx, len=64, padFrom='left') {
	if (hx.length < 64) {
		var pad = '0'.repeat(len - hx.length);
		if (padFrom == 'left') {
			hx = pad + hx;
		} else {
			hx = hx + pad;
		}
	}
	return hx;
}


/*
Format elliptic curve point as hex.
*/
function ellipticHex(a) {
	if (isEllipticIdentity(a)) {
		return [zeroPad(''),zeroPad('')];
	}
	return a.map(x=>zeroPad(x.toString(16)));
}


/*
Format elliptic curve point as BigIntXBigInt.
*/
function ellipticHexToBigInt(a) {
	return a.map(x=>util.hexToBigInt(x));
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
	var g = generatorPoint();
	return ellipticPower(g, k);
}


/*
Is point on secp256k1?
*/
function isOnCurve(a) {
	var G = ellipticOrder();
	return (util.mod(a[1]**2n - a[0]**3n - 7n, G) == 0n);
}


/*
secp256k1 private keygen.
*/
function privateKey() {
	var k0 = crypto.getRandomValues(new Uint8Array(32));
	var k = util.bytesToBigInt(k0);
	if ((k <= 100n) || (k >= generatorOrder())) {
		return privateKey();
	}
	return zeroPad(k.toString(16));
}


/*
Secp256k1 public keygen.
*/
function publicKey(privKey, index=0) {
	if (typeof(privKey) == 'string') {
		privKey = util.hexToBigInt(privKey);
	}
	var pubKey = generatorPower(privKey);
	return ellipticHex(pubKey);
}


/*
Secp256k1 key pair [private, public].
*/
function keyPair() {
	var k = privateKey();
	var pk = publicKey(k);
	return [k, pk];
}


/*
Secp256k1 signatures, from hex message digest
and hex or bigint private key.
k input for testing.
*/
function sign(hexMsg, privKey) {
	var n = generatorOrder();
	var e = util.hexToBigInt(hexMsg);
	var d = privKey;
	if (typeof(privKey) != 'bigint') {
		d = util.hexToBigInt(privKey);
	}
	var k = util.hexToBigInt(privateKey());
	var r = util.mod(generatorPower(k)[0], n);
	if (r == 0n) {
		throw 'secp256k1.sign.r.ZeroError';
	}
	var s = util.invMod(k, n) * util.mod(e + d*r, n);
	s = util.mod(s, n);
	if (s > n/2n) {
		s = n - s;
		if (s > n/2n) {
			throw 'secp256k1.sign.s.RangeError';
		}
	}
	if (s == 0n) {
		throw 'secp256k1.sign.s.ZeroError';
	}
	var signature = ellipticHex([r, s]);
	return signature;
}


/*
Secp256k1 signature verification, from hex message digest,
hex or bigint signature and hex or bigint public key.
*/
function verify(hexMsg, hexSig, pubKey) {
	var e = util.hexToBigInt(hexMsg);
	var intSig = ellipticHexToBigInt(hexSig);
	var r = intSig[0];
	var s = intSig[1];
	var Q = ellipticHexToBigInt(pubKey);
	var n = generatorOrder();
	if ((r < 1n) || (s < 1n) || (r >= n) || (s >= n)) {
		return false;
	}
	var c = util.invMod(s, n);
	var u1 = util.mod(e * c, n);
	var u2 = util.mod(r * c, n);
	var pt = ellipticAdd(generatorPower(u1), ellipticPower(Q, u2));
	var v = util.mod(pt[0], n);
	return v == r;
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
	keyPair: keyPair,
	sign: sign,
	verify: verify,
}


})();
