"""
Home rolled auth, never trust anyone.
"""

import base64
import datetime
import hashlib
import random
import secrets
import time


from cryptography.hazmat.primitives.ciphers.aead import AESGCM
import cachetools.func
import ecdsa


from flask import (
	make_response,
	redirect,
	render_template,
	request,
	current_app,
)


from util import sqlite


deviceid_len = 32
uid_len = 32
ukey_len = 32


def random_sleep(base=0.1, addl=0.1):
	"""
	Random sleeps to prevent auth attacks.
	"""
	time.sleep(base + addl*random.random())


def gen_deviceid():
	'''
	Generate a new deviceid.
	'''
	return secrets.token_hex(deviceid_len//2)


@cachetools.func.ttl_cache(ttl=12*3600)
def get_ukey_signature_key():
	"""
	Get a signing key for cookies.
	"""
	udb = sqlite.KV("udb")
	sk_b64 = udb.get("ukey_signature_key")
	uksm = udb.get("ukey_signature_month")

	now = datetime.datetime.now().date()
	this_month = now.strftime("%Y-%m-01")

	if uksm != this_month:
		sk_b64 = None # Generate a new key.
		udb.put("ukey_signature_month", this_month)

	if sk_b64 is None or sk_b64 == "":
		# New ukey_signature_key:
		sk = ecdsa.SigningKey.generate(ecdsa.SECP256k1)
		sk_b64 = base64.b64encode(sk.to_string()).decode()
		udb.put("ukey_signature_key", sk_b64)
	else:
		# Reconstruct ukey_signature from base64 encoding:
		sk_str = base64.b64decode(sk_b64)
		sk = ecdsa.SigningKey.from_string(sk_str, curve=ecdsa.SECP256k1)
	return sk


def hash_uid(uid):
	"""
	Hash for user_id/uid storage to database.
	"""
	salt0 = "y38m55d24v83x84r77s02"
	hash1x = hashlib.sha256((salt0 + uid).encode()).hexdigest()
	hash2x = hashlib.sha512((salt0 + hash1x + uid).encode()).hexdigest()
	hash3x = hashlib.sha256((salt0 + hash2x + uid).encode()).hexdigest()
	return hash3x[:uid_len//2]



def hash_ukey(ukey):
	"""
	Hash for ukey storage to database.
	"""
	salt0 = "e19n63c34r83y84p33t07"
	hash1x = hashlib.sha256((salt0 + ukey).encode()).hexdigest()
	hash2x = hashlib.sha512((salt0 + hash1x + ukey).encode()).hexdigest()
	hash3x = hashlib.sha256((salt0 + hash2x + ukey).encode()).hexdigest()
	return hash3x[:ukey_len]


def verify_ukey_chksum(uid, ukey):
	'''
	Verify user credentials checksum.
	'''
	assert len(uid) == uid_len
	assert len(ukey) == ukey_len
	ukey_parts = ukey.split('.')
	assert len(ukey_parts) == 3
	nonce_hex = ukey_parts[0]
	pad = ukey_parts[1]
	chksum = ukey_parts[2]
	chk = hashlib.sha256(bytes.fromhex(uid + pad)).hexdigest()[:8]
	assert chk == chksum
	return True


def verify_ukey_pow(uid, ukey, difficulty=15):
	'''
	Verify user credentials proof of work.
	'''
	nonce_hex = ukey.split('.')[0]
	xx = hashlib.sha512(hashlib.sha512(bytes.fromhex(uid)).digest()).hexdigest()
	hin = bytes.fromhex(xx + nonce_hex)
	hx = hashlib.sha256(hashlib.sha512(hashlib.sha256(hin).digest()).digest()).hexdigest()
	hxbin = bin(int(hx, 16))[3:][:difficulty]
	assert '0'*difficulty == hxbin
	return True


def gen_ukey_token(uid, ukey):
	"""
	Generate a token based on uid after ukey is checked.
	"""
	random_sleep()
	verify_ukey_chksum(uid, ukey)
	uid_hash = hash_uid(uid)
	ukey_hash = hash_ukey(ukey)
	udb_ukey_hash = sqlite.KV("udb").get(f"ukey_hash_{uid_hash}")
	if udb_ukey_hash is None:
		verify_ukey_pow(uid, ukey)
		sqlite.KV("udb").put(f"ukey_hash_{uid_hash}", ukey_hash)
	else:
		assert udb_ukey_hash == ukey_hash
	sk = get_ukey_signature_key()
	ukey_token = sk.sign(uid_hash.encode())
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
		uid_hash = hash_uid(uid)
		return vk.verify(ukey_token, uid_hash.encode())
	except:
		return False


def hash_ekey(ekey):
	"""
	Mapping from database encryption key to actual encryption key.
	"""
	salt0 = "e661n341c738r920y771p332t"
	hash1x = hashlib.sha256((salt0 + ekey).encode()).hexdigest()
	hash2x = hashlib.sha256((salt0 + hash1x + ekey).encode()).hexdigest()
	hash3x = hashlib.sha256((salt0 + hash2x + ekey).encode()).hexdigest()
	return hash3x


@cachetools.func.ttl_cache(ttl=12*3600)
def get_lt_encryption_key():
	"""
	Get an encryption key for long term storage.
	"""
	udb = sqlite.KV("udb")
	ltek = udb.get("lt_encryption_key")
	if ltek is None or ltek == "":
		ltek = secrets.token_hex(32)
		udb.put("lt_encryption_key", ltek)
	return hash_ekey(ltek)


def lt_encrypt(msg):
	"""
	Encryption for long term storage.
	"""
	if (msg is None) or (msg == ""):
		return msg
	lt_key = get_lt_encryption_key()
	aesgcm = AESGCM(bytes.fromhex(lt_key))
	enc_raw = aesgcm.encrypt(b"nonce", msg.encode(), b"addl")
	enc_b64 = base64.b64encode(enc_raw).decode()
	return enc_b64


def lt_decrypt(enc_b64):
	"""
	Encryption for long term storage.
	"""
	if (enc_b64 is None) or (enc_b64 == ""):
		return enc_b64
	lt_key = get_lt_encryption_key()
	aesgcm = AESGCM(bytes.fromhex(lt_key))
	enc_raw = base64.b64decode(enc_b64.encode())
	msg_raw = aesgcm.decrypt(b"nonce", enc_raw, b"addl")
	return msg_raw.decode()


def is_verified():
	"""
	Flask check cookies for user auth verification.
	"""
	ans = True
	if ("uid" not in request.cookies) or ("ukey_token" not in request.cookies):
		return False

	uid = request.cookies.get("uid")
	assert len(uid) == uid_len
	ukey_token = request.cookies.get("ukey_token")

	return verify_ukey_token(uid, ukey_token)


def unverified_redirect():
	"""
	Flask redirect to login.
	"""
	return make_response(redirect("/login", code=302))


def verified_response(template_name, content={}):
	"""
	Flask response with auth verification.
	"""
	if not is_verified():
		return unverified_redirect()

	return make_response(render_template(template_name, **content))

