/*
Leprechaun Sauce
*/


function dateTime(id) {
	var date = new Date();
	document.getElementById(id).innerHTML = date.toISOString().slice(0, -5).replace("T", "_");
	setTimeout('date_time("' + id + '");', '1000');
	return true;
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
	return new Uint8Array([79, 159, 147, 28, 195, 193, 197, 30, 25, 127, 1, 66]);
}


async function padString(msg) {
	strLen = msg.length;
	padding = await btoa(sha512(msg + pubSalt()));
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
	msg = await padString(msg);
	msg = (new TextEncoder()).encode(msg).buffer;
	encr = await crypto.subtle.encrypt(aesgcm, akey, msg);
	return btoa(encr);
}

async function decrypt(msg, akey) {
	/*wip*/
	aesgcm = aesgcmParams();
	akey = await deriveKey(akey);
	//msg = (new TextEncoder()).encode(atob(msg)).buffer;
	msg = Uint8Array.from(atob(msg), c => c.charCodeAt(0));
	decr = await crypto.subtle.decrypt(aesgcm, akey, msg);
	//decr = await unpadString(decr);
	return decr;
}


