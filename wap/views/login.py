#!/usr/bin/env python3

import base64
import datetime
import json
import time
import hashlib
import secrets
import random

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
	sk_b64 = rock.rocks("udb", read_only=True).get("ukey_signature_key")
	if sk_b64 is None or sk_b64 == "":
		sk = ecdsa.SigningKey.generate(ecdsa.SECP256k1)
		sk_b64 = base64.b64encode(sk.to_string()).decode()
		rock.rocks("udb").put("ukey_signature_key", sk_b64)
	else:
		sk_str = base64.b64decode(sk_b64)
		sk = ecdsa.SigningKey.from_string(sk_str, curve=ecdsa.SECP256k1)
	return sk


def gen_ukey_token(uid):
	sk = get_ukey_signature_key()
	ukey_token = sk.sign(uid.encode())
	ukey_token_b64 = base64.b64encode(ukey_token).decode()
	return ukey_token_b64


def validate_ukey_token(uid, ukey_token_b64):
	sk = get_ukey_signature_key()
	vk = sk.get_verifying_key()
	ukey_token = base64.b64decode(ukey_token_b64)
	return vk.verify(ukey_token, uid.encode())


@login_blueprint.route("/login/", methods=["GET"])
def login():

	time.sleep(0.1 + 0.1*random.random())
	content = {}

	if "deviceid" not in request.cookies:
		current_app.logger.info(f"login:nocookies")
		return make_response(render_template("cookies.html", **content))
	deviceid = request.cookies.get("deviceid")
	if ("uid" in request.cookies) and ("ukey_token" in request.cookies):
		uid = request.cookies.get("uid")
		ukey_token = request.cookies.get("ukey_token")
		current_app.logger.info(f"login:uid:{uid}:ukey_token:{ukey_token}")
		if validate_ukey_token(uid, ukey_token):
			current_app.logger.info(f"login:success:uid:{uid}")
			return make_response(redirect("/", code=302))
		current_app.logger.info(f"login:fail:uid:{uid}")
	current_app.logger.info(f"login:new:deviceid:{deviceid}")
	return make_response(render_template("login.html", **content))


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


