/*
Leprechaun B, no rights reserved.
*/

var util = (function () {


/*
Bind the time to html.
*/
function dateTime(id) {
	var date = new Date();
	document.getElementById(id).innerHTML = date.toISOString().slice(0, -5).replace('T', '_');
	setTimeout('util.dateTime("' + id + '");', '1000');
	return true;
}


/*
Sleep, to suspend the drawing thread. Used to induce flicker when screen painting encryption/decryption.
*/
async function sleep(ms) {
	return await new Promise(x => setTimeout(x, ms));
}


/*
Time a nullary function, use a lambda to set parameters.
*/
async function timeit(func) {
	a = performance.now();
	res = await func();
	b = performance.now();
	d = (b - a) / 1000.0;
	console.log('Call to ' + func + ' took: ' + d + ' seconds.');
	return res;
}


/*
Random bytes.
*/
function randomBytes(n) {
	return crypto.getRandomValues(new Uint8Array(n));
}


/*
Random hex.
*/
function randomHex(n) {
	return bytesToHex(randomBytes(Math.floor(n/2+1))).slice(0,n);
}


/*
Generate a list of bytes in the range.
*/
function byteRange(start, stop, step=1) {
	raw = [start];
	x = start;
	while (true) {
		x += step;
		if (x > stop) {
			break;
		}
		raw.push(x);
	}
	return new Uint8Array(raw);
}


/*
bytes to hex.
*/
function bytesToHex(byteArray) {
	return Array.from(new Uint8Array(byteArray), function(byte) {
		return ('0' + (byte & 0xFF).toString(16)).slice(-2);
	}).join('');
}


/*
hex to bytes
*/
function hexToBytes(hexString) {
	var result = [];
	for (var i = 0; i < hexString.length; i += 2) {
		result.push(parseInt(hexString.substr(i, 2), 16));
	}
	return (new Uint8Array(result));
}


/*
hex to base64
*/
function hexToBase64(hexstring) {
	return btoa(hexstring.match(/\w{2}/g).map(function(a) {
		return String.fromCharCode(parseInt(a, 16));
	}).join(''));
}


/*
base64 to hex
*/
function base64ToHex(base64) {
	var raw = atob(base64);
	var HEX = '';
	for ( i = 0; i < raw.length; i++ ) {
		var _hex = raw.charCodeAt(i).toString(16);
		HEX += (_hex.length==2?_hex:'0'+_hex);
	}
	return HEX.toLowerCase();
}


/*
Bytes to BigInt
*/
function bytesToBigInt(x) {
	x = x.reverse();
	y = 0n;
	M = BigInt(x.length);
	for (i=0n; i<M; i++) {
		y += BigInt(x[i]) * bigPow(2n, 8n*i);
	}
	return y;
}


/*
BigInt to Hex
*/
function bigIntToHex(x) {
	hx = x.toString(16);
	if (hx.length % 2 != 0) {
		hx = '0' + hx;
	}
	return hx;
}


/*
Hex to BigInt
*/
function hexToBigInt(x) {
	return bytesToBigInt(hexToBytes(x));
}


/*
BigInt to Bytes
*/
function bigIntToBytes(x) {
	asHex = bigIntToHex(x);
	return hexToBytes(asHex);
}


/*
Bytes to Base58
*/
function bytesToBase58(b58) {
	A = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz';
	var d = [], s = '', i, j, c, n;
	for(i in b58) {
		j = 0,
		c = b58[i];
		s += c || s.length ^ i ? '' : 1;
		while(j in d || c) {
			n = d[j];
			n = n ? n * 256 + c : c;
			c = n / 58 | 0;
			d[j] = n % 58;
			j++;
		}
	}
	while (j--) {
		s += A[d[j]];
	}
	return s;
}


/*
Base58 to Bytes.
*/
function base58ToBytes(b58) {
	A = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz';
	var d = [], b = [], i, j, c, n;
	for(i in b58) {
		j = 0,
		c = A.indexOf(b58[i]);
		if(c < 0)
			return undefined;
		c || b.length ^ i ? i : b.push(0);
		while(j in d || c) {
			n = d[j];
			n = n ? n * 58 + c : c;
			c = n >> 8;
			d[j] = n % 256;
			j++;
		}
	}
	while (j--) {
		b.push(d[j]);
	}
	return new Uint8Array(b);
}


/*
Modulo function for javascript, % is incorrect.
*/
function mod(n, m) {
	return ((n % m) + m) % m;
}


/*
Modular Inverse function.
*/
function invMod(a, b) {
	a = BigInt(a);
	b = BigInt(b);
	inv1 = 1n;
	inv2 = 0n;
	while ((b != 1n) && (b != 0n)) {
		s = inv1;
		inv1 = inv2;
		inv2 = s - inv2 * (a / b);
		s = a;
		a = b;
		b = mod(s, b);
	}
	return inv2;
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
		a = mod(a, b);
		if (a == 0) {
			return b;
		}
		b %= a;
	}
}


/*
sha256 short.
*/
function sha256(msg) {
	if (typeof msg == 'string') {
		msg = (new TextEncoder()).encode(msg);
	}
	return crypto.subtle.digest('SHA-256', msg);
}


/*
sha512 short.
*/
function sha512(msg) {
	if (typeof msg == 'string') {
		msg = (new TextEncoder()).encode(msg);
	}
	return crypto.subtle.digest('SHA-512', msg);
}


/*
AES-GCM 256 public salt.
Chosen in a predictable manner, based on the golden prime.
*/
function pubSaltArray(len=16) {
	return byteRange(79, 79 + len - 1);
}


/*
AES-GCM 256 public initalization vector.
Chosen in a predictable manner, based on the golden prime.
*/
function pubIV(len=12) {
	return byteRange(79, 79 + len - 1);
}


/*
AES-GCM helper.
*/
function aesgcmParams() {
	aesgcm = {
		'name': 'AES-GCM',
		'iv': pubIV(),
		'tagLength': 128,
	}
	return aesgcm;
}


/*
AES-GCM 256 key derivation.
*/
async function deriveKey(akey) {
	akey = await crypto.subtle.importKey(
		'raw',
		(new TextEncoder()).encode(akey),
		{
			'name': 'PBKDF2',
		},
		false,
		['deriveBits', 'deriveKey']
	);
	return await crypto.subtle.deriveKey(
	{
		'name': 'PBKDF2',
		'salt': pubSaltArray(),
		'iterations': 9999,
		'hash': 'SHA-512',
	},
	akey,
	{
		'name': 'AES-GCM',
		'length': 256,
	},
	false,
	['encrypt', 'decrypt']);
}


/*
Weak AES encrytion.
*/
async function encrypt(msg, akey) {
	if (msg === '') {
		return '';
	}
	aesgcm = aesgcmParams();
	akey = await deriveKey(akey);
	msg = (new TextEncoder()).encode(msg);
	encr = await crypto.subtle.encrypt(aesgcm, akey, msg);
	encr = bytesToHex(encr);
	encr = hexToBase64(encr);
	return encr;
}


/*
Weak AES decrytion.
*/
async function decrypt(msg, akey) {
	if (msg === '') {
		return '';
	}
	aesgcm = aesgcmParams();
	akey = await deriveKey(akey);
	msg = base64ToHex(msg);
	msg = hexToBytes(msg);
	decr = await crypto.subtle.decrypt(aesgcm, akey, msg);
	decr = (new TextDecoder()).decode(decr);
	return decr;
}


/*
Get/cache a local encryption key for e2ee.
*/
async function localKey() {
	lkey = localStorage.getItem('local_key')
	if (!lkey) {
		lkey = prompt('local_key:', '');
		lkey = hexToBase64(bytesToHex(await sha256(lkey)));
		lkey = await encrypt(lkey, 'local_key' + lkey);
		localStorage.setItem('local_key', lkey);
	}
	return lkey;
}


/*
Submit encrypted form data.
*/
async function encryptedSubmitForm(formName) {
	ekey = await localKey();
	form = document.forms[formName];
	form_types = [];
	for (idx=0; idx < form.elements.length; idx += 1) {
		dtype = form.elements[idx].type
		form_types.push(dtype)
		form.elements[idx].type = 'text'
		form.elements[idx].value = await encrypt(form.elements[idx].value, ekey);
		await sleep(2);
	}
	form.submit();
	for (idx=0; idx < form.elements.length; idx += 1) {
		await sleep(2);
		form.elements[idx].type = form_types[idx];
		form.elements[idx].value = await decrypt(form.elements[idx].value, ekey);
	}
}


/*
Decrypt html element text content of class encrypted.
*/
async function decryptElements() {
	ekey = await localKey();
	cts = document.getElementsByClassName('encrypted');
	for (ct of cts) {
		ct.textContent = await decrypt(ct.textContent, ekey);
	}
}


/*
Big Square Root function.
*/
function bigSqrt(n) {
	m = BigInt(n);
	if (m < 0n) {
		throw 'nope';
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
	} else if (mod(b, 2n) == 1n) {
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
Proof of work for new account credentials.
*/
async function proofOfWork(hx, difficulty=15) {
	hx = bytesToHex(await sha512(await sha512(hexToBytes(hx))));
	check = '0'.repeat(difficulty);
	nonce = 0n;
	while (true) {
		nonceHex = bigIntToHex(nonce);
		hashInput = hexToBytes(hx + nonceHex);
		hash1 = bytesToHex(await sha256(await sha512(await sha256(hashInput))));
		hash2 = hexToBigInt(hash1).toString(2).slice(1, difficulty + 1);
		if (hash2 == check) {
			return nonceHex;
		}
		nonce++;
	}
}


/*
New userId.
*/
function generateUserId() {
	return randomHex(32);
}


/*
New userKey.
*/
async function generateUserKey(userId, len=32, checkLen=8) {
	nonceHex = await proofOfWork(userId);
	padLen = len - nonceHex.length - 2 - checkLen;
	pad = randomHex(padLen);
	check = bytesToHex(await sha256(hexToBytes(userId + pad))).slice(0, checkLen);
	key = nonceHex + '.' + pad + '.' + check;
	return key;
}


return {
	dateTime: dateTime,
	sleep: sleep,
	timeit: timeit,
	randomBytes: randomBytes,
	randomHex: randomHex,
	byteRange: byteRange,
	bytesToHex: bytesToHex,
	hexToBytes: hexToBytes,
	hexToBase64: hexToBase64,
	base64ToHex: base64ToHex,
	bytesToBigInt: bytesToBigInt,
	bigIntToHex: bigIntToHex,
	hexToBigInt: hexToBigInt,
	bigIntToBytes: bigIntToBytes,
	bytesToBase58: bytesToBase58,
	base58ToBytes: base58ToBytes,
	mod: mod,
	invMod: invMod,
	gcd: gcd,
	sha256:sha256,
	sha512:sha512,
	encrypt: encrypt,
	decrypt: decrypt,
	localKey: localKey,
	encryptedSubmitForm: encryptedSubmitForm,
	decryptElements: decryptElements,
	bigSqrt: bigSqrt,
	bigPow: bigPow,
	bigAbs: bigAbs,
	proofOfWork: proofOfWork,
	generateUserId: generateUserId,
	generateUserKey: generateUserKey,
}


})();
