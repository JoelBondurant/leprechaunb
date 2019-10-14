"""
Home rolled auth, never trust anyone.
"""

import base64
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


def gen_deviceid():
	return secrets.token_hex(16)


def gen_uid():
	return secrets.token_hex(8)


def gen_ukey():
	return secrets.token_hex(8)


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


def gen_ukey_token(uid, ukey, new_ukey=False):
	"""
	Generate a token based on uid after ukey is checked.
	"""
	random_sleep()
	if new_ukey:
		sqlite.KV("udb").put(f"ukey_{uid}", ukey)
	else:
		udb_ukey = sqlite.KV("udb").get(f"ukey_{uid}")
		assert udb_ukey == ukey
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
	return vk.verify(ukey_token, uid.encode())


