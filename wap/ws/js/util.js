/*
Leprechaun Sauce
*/


function dateTime(id) {
	var date = new Date();
	document.getElementById(id).innerHTML = date.toISOString().slice(0, -5).replace("T", "_");
	setTimeout('dateTime("' + id + '");', '1000');
	return true;
}


async function sleep(ms) {
	return await new Promise(x => setTimeout(x, ms));
}


function uint8range(start, stop, step=1) {
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


async function getAddressBalance(addr, confirmations=6) {
	base = "https://blockchain.info/q/addressbalance/";
	resp = await fetch(base + addr + "?confirmations=" + confirmations);
	return resp.json();
}


function uint8ArrayToHex(byteArray) {
	return Array.from(new Uint8Array(byteArray), function(byte) {
		return ("0" + (byte & 0xFF).toString(16)).slice(-2);
	}).join("");
}


function hexToUint8Array(hexString) {
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


function pubSaltArray(len=16) {
	return uint8range(79, 79 + len - 1);
}


function pubIV(len=12) {
	return uint8range(79, 79 + len - 1);
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
	if (msg === "") {
		return "";
	}
	aesgcm = aesgcmParams();
	akey = await deriveKey(akey);
	msg = (new TextEncoder()).encode(msg);
	encr = await crypto.subtle.encrypt(aesgcm, akey, msg);
	encr = uint8ArrayToHex(encr);
	encr = hexToBase64(encr);
	return encr;
}


async function decrypt(msg, akey) {
	if (msg === "") {
		return "";
	}
	aesgcm = aesgcmParams();
	akey = await deriveKey(akey);
	msg = base64ToHex(msg);
	msg = hexToUint8Array(msg);
	decr = await crypto.subtle.decrypt(aesgcm, akey, msg);
	decr = (new TextDecoder()).decode(decr);
	return decr;
}


async function localKey() {
	lkey = localStorage.getItem("local_key")
	if (!lkey) {
		lkey = prompt("local_key:", "");
		lkey = hexToBase64(uint8ArrayToHex(await sha256(lkey)));
		lkey = await encrypt(lkey, "local_key" + lkey);
		localStorage.setItem("local_key", lkey);
	}
	return lkey;
}


async function encryptedSubmitForm(formName) {
	ekey = await localKey();
	form = document.forms[formName];
	form_types = [];
	for (idx=0; idx < form.elements.length; idx += 1) {
		dtype = form.elements[idx].type
		form_types.push(dtype)
		form.elements[idx].type = "text"
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


async function decryptElements() {
	ekey = await localKey();
	cts = document.getElementsByClassName("encrypted");
	for (ct of cts) {
		ct.textContent = await decrypt(ct.textContent, ekey);
	}
}

