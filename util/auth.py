"""
Home rolled auth, never trust anyone.
"""

import base64
import hashlib
import random
import secrets
import time

import cachetools.func
import ecdsa

from util import sqlite


def random_sleep(base=0.1, addl=0.1):
	"""
	Random sleeps to prevent auth attacks.
	"""
	time.sleep(base + addl*random.random())


deviceid_len = 32
def gen_deviceid():
	return secrets.token_hex(deviceid_len//2)


uid_len = 16
def gen_uid():
	return secrets.token_hex(uid_len//2)


ukey_len = 16
def gen_ukey():
	return secrets.token_hex(ukey_len//2)


@cachetools.func.ttl_cache(ttl=12*3600)
def get_ukey_signature_key():
	"""
	Get a signing key for cookies.
	"""
	sk_b64 = sqlite.KV("udb").get("ukey_signature_key")
	if sk_b64 is None or sk_b64 == "":
		sk = ecdsa.SigningKey.generate(ecdsa.SECP256k1)
		sk_b64 = base64.b64encode(sk.to_string()).decode()
		sqlite.KV("udb").put("ukey_signature_key", sk_b64)
	else:
		sk_str = base64.b64decode(sk_b64)
		sk = ecdsa.SigningKey.from_string(sk_str, curve=ecdsa.SECP256k1)
	return sk


def hash_ukey(akey):
	salt0 = "19c6dc34e838f330"
	salt1 = hashlib.sha256((salt0 + akey).encode()).hexdigest()
	hashedup = hashlib.sha256((salt0 + akey).encode()).hexdigest()
	hashedup2x = hashlib.sha256((salt1 + hashedup).encode()).hexdigest()
	return hashedup2x[:ukey_len]


def gen_ukey_token(uid, ukey, new_ukey=False):
	"""
	Generate a token based on uid after ukey is checked.
	"""
	random_sleep()
	ukey_hash = hash_ukey(ukey)
	if new_ukey:
		sqlite.KV("udb").put(f"ukey_hash_{uid}", ukey_hash)
	else:
		udb_ukey_hash = sqlite.KV("udb").get(f"ukey_hash_{uid}")
		assert udb_ukey_hash == ukey_hash
	sk = get_ukey_signature_key()
	ukey_token = sk.sign(uid.encode())
	ukey_token_b64 = base64.b64encode(ukey_token).decode()
	return ukey_token_b64


def verify_ukey_token(uid, ukey_token_b64):
	"""
	Validate a ukey token.
	"""
	random_sleep()
	sk = get_ukey_signature_key()
	vk = sk.get_verifying_key()
	ukey_token = base64.b64decode(ukey_token_b64)
	try:
		return vk.verify(ukey_token, uid.encode())
	except:
		return False


