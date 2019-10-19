/*
Leprechaun Sauce
*/


function dateTime(id) {
	var date = new Date();
	document.getElementById(id).innerHTML = date.toISOString().slice(0, -5).replace("T", "_");
	setTimeout('dateTime("' + id + '");', '1000');
	return true;
}


function uint8ArrayToHexString(byteArray) {
	return Array.from(new Uint8Array(byteArray), function(byte) {
		return ("0" + (byte & 0xFF).toString(16)).slice(-2);
	}).join("");
}


function hexStringToUint8Array(hexString) {
	var result = [];
	for (var i = 0; i < hexString.length; i += 2) {
		result.push(parseInt(hexString.substr(i, 2), 16));
	}
	return new Uint8Array(result);
}


function hexToBase64(hexstring) {
	return btoa(hexstring.match(/\w{2}/g).map(function(a) {
		return String.fromCharCode(parseInt(a, 16));
	}).join(""));
}


function base64ToHex(base64) {
	var raw = atob(base64);
	var HEX = '';
	for ( i = 0; i < raw.length; i++ ) {
		var _hex = raw.charCodeAt(i).toString(16);
		HEX += (_hex.length==2?_hex:'0'+_hex);
	}
	return HEX.toLowerCase();
}


function sha256(msg) {
	return crypto.subtle.digest("SHA-256", (new TextEncoder()).encode(msg));
}


function sha512(msg) {
	return crypto.subtle.digest("SHA-512", (new TextEncoder()).encode(msg));
}


function pubSaltArray() {
	return new Uint8Array([79, 83, 33, 212, 19, 1, 13, 84, 22, 70, 8, 9, 1, 2, 3, 4]);
}


function pubIV() {
	return new Uint8Array([79, 83, 33, 128, 195, 193, 197, 3, 25, 127, 20, 9]);
}


function aesgcmParams() {
	aesgcm = {
		"name": "AES-GCM",
		"iv": pubIV(),
		"tagLength": 128,
	}
	return aesgcm;
}


async function deriveKey(akey) {
	akey = await crypto.subtle.importKey(
		"raw",
		(new TextEncoder()).encode(akey),
		{
			"name": "PBKDF2",
		},
		false,
		["deriveBits", "deriveKey"]
	);
	return await crypto.subtle.deriveKey(
	{
		"name": "PBKDF2",
		"salt": pubSaltArray(),
		"iterations": 9999,
		"hash": "SHA-512",
	},
	akey,
	{
		"name": "AES-GCM",
		"length": 256,
	},
	false,
	["encrypt", "decrypt"]);
}


async function encrypt(msg, akey) {
	aesgcm = aesgcmParams();
	akey = await deriveKey(akey);
	msg = (new TextEncoder()).encode(msg);
	encr = await crypto.subtle.encrypt(aesgcm, akey, msg);
	encr = uint8ArrayToHexString(encr);
	encr = hexToBase64(encr);
	return encr;
}


async function decrypt(msg, akey) {
	aesgcm = aesgcmParams();
	akey = await deriveKey(akey);
	msg = base64ToHex(msg);
	msg = hexStringToUint8Array(msg);
	decr = await crypto.subtle.decrypt(aesgcm, akey, msg);
	decr = (new TextDecoder()).decode(decr);
	return decr;
}


