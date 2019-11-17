/*
dev wip
*/

var dev = (function () {


async function verifyUserKey(userId, userKey, difficulty=4, checkLen=8) {
	userKeyParts = userKey.split('.');
	nonceCheck = false;
	x = new Uint8Array(await util.sha512(await util.sha512(userId)));
	nonce = util.hexToBigInt(userKeyParts[0])
	nonceBytes = util.bigIntToBytes(nonce);
	hsh = await util.sha256(await util.sha512(await util.sha256(x + nonceBytes)));
	hshZero = new Uint8Array(hsh.slice(0, difficulty));
	depth = 0;
	for (idx=0; idx<hshZero.length; idx++) {
		hp = hshZero[idx];
		if (hp == 0) {
			depth += 2;
			continue;
		} else if (hp < 16) {
			depth += 1;
		}
		break;
	}
	if (depth >= difficulty) {
		nonceCheck = true;
	}
	pad = userKeyParts[1];
	check = util.bytesToHex(await util.sha256(userId + pad)).slice(0, checkLen);
	check = (check == userKeyParts[2]);
	return check && nonceCheck;
}


async function proofOfWork(x, difficulty=4) {
	x = new Uint8Array(await util.sha512(await util.sha512(x)));
	nonce = 0n;
	while (true) {
		nonceBytes = util.bigIntToBytes(nonce);
		hsh = await util.sha256(await util.sha512(await util.sha256(x + nonceBytes)));
		hshZero = new Uint8Array(hsh.slice(0, difficulty));
		depth = 0;
		for (idx=0; idx<hshZero.length; idx++) {
			hp = hshZero[idx];
			if (hp == 0) {
				depth += 2;
				continue;
			} else if (hp < 16) {
				depth += 1;
			}
			break;
		}
		if (depth >= difficulty) {
			return nonce;
		}
		nonce++;
	}
}

function randomBytes(n) {
	return crypto.getRandomValues(new Uint8Array(n));
}


function randomHex(n) {
	return util.bytesToHex(randomBytes(Math.floor(n/2+1))).slice(0,n);
}


function generateUserId() {
	return randomHex(32);
}


async function generateUserKey(userId, len=32, checkLen=8) {
	nonce = (await proofOfWork(userId)).toString(16);
	padLen = len - nonce.length - 2 - checkLen;
	pad = randomHex(padLen);
	check = util.bytesToHex(await util.sha256(userId + pad)).slice(0, checkLen);
	key = nonce + '.' + pad + '.' + check;
	return key;
}

return {
	proofOfWoirk: proofOfWork,
	randomBytes: randomBytes,
	randomHex: randomHex,
	verifyUserKey: verifyUserKey,
	generateUserId: generateUserId,
	generateUserKey: generateUserKey,
}

})();
