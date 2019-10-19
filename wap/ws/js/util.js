/*
Leprechaun Sauce
*/


function dateTime(id) {
	var date = new Date();
	document.getElementById(id).innerHTML = date.toISOString().slice(0, -5).replace("T", "_");
	setTimeout('date_time("' + id + '");', '1000');
	return true;
}


function toBase64(blob) {
	return btoa(encodeURIComponent(blob).replace(/%([0-9A-F]{2})/g,
		function toSolidBytes(match, p1) {
			return String.fromCharCode("0x" + p1);
		}
	));
}


function fromBase64(msg) {
	return decodeURIComponent(atob(msg).split("").map(function(c) {
		return "%" + ("00" + c.charCodeAt(0).toString(16)).slice(-2);
	}).join(""));
}


function sha256(msg) {
	return crypto.subtle.digest("SHA-256", (new TextEncoder()).encode(msg));
}


function sha512(msg) {
	return crypto.subtle.digest("SHA-512", (new TextEncoder()).encode(msg));
}


function pubSalt() {
	return "leprechaunbsalt"
}


function pubIV() {
	return new Uint8Array([79, 83, 33, 128, 195, 193, 197, 3, 25, 127, 20, 9]);
}


async function padString(msg) {
	padding = await toBase64(sha512(msg + pubSalt()));
	return msg + padding.repeat(10);
}


async function unpadString(msg) {
	return msg.slice(0, -240);
}


function aesgcmParams() {
	aesgcm = {
		"name": "AES-GCM",
		"iv": pubIV(),
		"length": 256,
		"tagLength": 128,
	}
	return aesgcm;
}


async function deriveKey(akey0) {
	aesgcm = aesgcmParams();
	akey = await sha256(sha512(akey0 + pubSalt()));
	akey = await crypto.subtle.importKey("raw", akey, aesgcm, false, ["encrypt", "decrypt"]);
	return akey;
}


async function encrypt(msg, akey) {
	/*wip*/
	aesgcm = aesgcmParams();
	akey = await deriveKey(akey);
	msg = toBase64(msg);
	msg = await padString(msg);
	msg = (new TextEncoder()).encode(msg);
	encr = await crypto.subtle.encrypt(aesgcm, akey, msg);
	return toBase64(encr);
}


async function decrypt(msg, akey) {
	/*wip*/
	aesgcm = aesgcmParams();
	akey = await deriveKey(akey);
	msg1 = fromBase64(msg);
	msg2 = Uint8Array.from(msg1, c => c.charCodeAt(0));
	decr = await crypto.subtle.decrypt(aesgcm, akey, msg2);
	//decr = fromBase64(decr)
	//decr = await unpadString(decr);
	return [msg, msg1, msg2, decr];
}


