#!/usr/bin/env python3
import datetime
import json
import time
import hashlib
import secrets

import cachetools.func
import ecdsa

from flask import (
	Blueprint,
	current_app,
	make_response,
	redirect,
	render_template,
	request,
	send_from_directory,
)

from util import rock


login_blueprint = Blueprint("login", __name__)


@cachetools.func.ttl_cache(ttl=6*3600)
def get_ukey_signature_key():
	uksk_hex = rock.rocks("udb", read_only=True).get("ukey_signature_key")
	if uksk_hex is None:
		uksk = ecdsa.SigningKey.generate(ecdsa.SECP256k1)
		uksk_hex.to_string().hex()
		rock.rocks("udb").put("ukey_signature_key", uksk_hex)
	else:
		uksk = ecdsa.SigningKey.from_string(binascii.unhexlify(uksk_hex), curve=ecdsa.SECP256k1)
	return uksk


def gen_ukey_token(uid):
	uksk = get_ukey_signature_key()
	ukey_token = uksk.sign(uid.encode()).hex()
	return ukey_token



@login_blueprint.route("/login/", methods=["GET"])
def login():

	time.sleep(0.1)
	content = {}

	if "deviceid" not in request.cookies:
		resp = make_response(render_template("cookies.html", **content))
	else:
		resp = make_response(render_template("login.html", **content))

	return resp


@login_blueprint.route("/login/new/", methods=["GET", "POST"])
def login_new():

	time.sleep(0.1)
	if "deviceid" not in request.cookies:
		return "enable cookies."

	deviceid = request.cookies.get("deviceid")
	assert len(deviceid) == 32

	uid = secrets.token_hex(8)
	current_app.logger.info(f"new:uid:{uid}")

	ukey = secrets.token_hex(8)

	rock.rocks("udb").put(f"ukey_{uid}", ukey)

	content = {
		"deviceid": deviceid,
		"uid": uid,
		"ukey": ukey,
	}

	resp = make_response(render_template("new.html", **content))

	expires = datetime.datetime.now() + datetime.timedelta(days=365)
	resp.set_cookie("uid", uid, expires=expires, samesite="strict")

	expires = datetime.datetime.now() + datetime.timedelta(days=28)
	ukey_token = gen_ukey_token(uid)
	resp.set_cookie("ukey_token", ukey_token, expires=expires, samesite="strict")

	return resp


@login_blueprint.route("/login/verify/", methods=["POST"])
def login_verify():

	time.sleep(0.1)
	if "deviceid" not in request.cookies:
		return "enable cookies."

	deviceid = request.cookies.get("deviceid")
	assert len(deviceid) == 32

	uid = request.form.get("uid")
	assert len(uid) == 16

	ukey = request.form.get("ukey")
	assert len(ukey) == 16

	udb_ukey = rock.rocks("udb", read_only=True).get(f"ukey_{uid}")
	assert udb_ukey == ukey

	resp = make_response(redirect("/", code=302))

	expires = datetime.datetime.now() + datetime.timedelta(days=365)
	resp.set_cookie("uid", uid, expires=expires, samesite="strict")

	expires = datetime.datetime.now() + datetime.timedelta(days=28)
	ukey_token = gen_ukey_token(uid)
	resp.set_cookie("ukey_token", ukey_token, expires=expires, samesite="strict")

	return resp


