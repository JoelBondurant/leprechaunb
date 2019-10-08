#!/usr/bin/env python3
import datetime
import json
import time
import hashlib
import secrets

from util import rock


from flask import (
	Blueprint,
	current_app,
	make_response,
	redirect,
	render_template,
	request,
	send_from_directory,
)


login_blueprint = Blueprint("login", __name__)



@login_blueprint.route("/login/", methods=["GET"])
def login():

	time.sleep(0.1)
	if "deviceid" not in request.cookies:
		return "enable cookies."

	content = {}

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
	resp.set_cookie("ukey", ukey, expires=expires, samesite="strict")

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

	udb_ukey = rock.rocks("udb").get(f"ukey_{uid}")
	assert udb_ukey == ukey

	resp = make_response(redirect("/", code=302))
	expires = datetime.datetime.now() + datetime.timedelta(days=365)
	resp.set_cookie("uid", uid, expires=expires, samesite="strict")
	expires = datetime.datetime.now() + datetime.timedelta(days=28)
	resp.set_cookie("ukey", ukey, expires=expires, samesite="strict")
	return resp


