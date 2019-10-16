#!/usr/bin/env python3

import datetime


from flask import (
	Blueprint,
	current_app,
	make_response,
	redirect,
	render_template,
	request,
	send_from_directory,
)


from util import auth


login_blueprint = Blueprint("login", __name__)



@login_blueprint.route("/login/", methods=["GET"])
def login():

	content = {}

	if "deviceid" not in request.cookies:
		current_app.logger.info(f"login:nocookies")
		return make_response(render_template("cookies.html", **content))

	deviceid = request.cookies.get("deviceid")
	if ("uid" in request.cookies) and ("ukey_token" in request.cookies):
		uid = request.cookies.get("uid")
		ukey_token = request.cookies.get("ukey_token")
		current_app.logger.info(f"login:uid:{uid}:ukey_token:{ukey_token}")
		if auth.verify_ukey_token(uid, ukey_token):
			current_app.logger.info(f"login:success:uid:{uid}")
			return make_response(redirect("/", code=302))
		current_app.logger.info(f"login:fail:uid:{uid}")
	current_app.logger.info(f"login:new:deviceid:{deviceid}")
	return make_response(render_template("login.html", **content))


@login_blueprint.route("/login/verify/", methods=["POST"])
def login_verify():

	if "deviceid" not in request.cookies:
		return "enable cookies."

	deviceid = request.cookies.get("deviceid")
	assert len(deviceid) == 32

	uid = request.form.get("user_id")
	assert len(uid) == 16

	ukey = request.form.get("remote_key")
	assert len(ukey) == 16

	ukey_token = auth.gen_ukey_token(uid, ukey)

	resp = make_response(redirect("/", code=302))

	expires = datetime.datetime.now() + datetime.timedelta(days=180)
	resp.set_cookie("uid", uid, expires=expires, samesite="strict", domain=".leprechaunb.com")

	expires = datetime.datetime.now() + datetime.timedelta(days=28)
	resp.set_cookie("ukey_token", ukey_token, expires=expires, samesite="strict", domain=".leprechaunb.com")

	return resp


@login_blueprint.route("/login/new/", methods=["GET", "POST"])
def login_new():

	if "deviceid" not in request.cookies:
		return "enable cookies."

	deviceid = request.cookies.get("deviceid")
	assert len(deviceid) == 32

	uid = auth.gen_uid()
	current_app.logger.info(f"new:uid:{uid}")

	ukey = auth.gen_ukey()

	ukey_token = auth.gen_ukey_token(uid, ukey, new_ukey=True)

	content = {
		"deviceid": deviceid,
		"uid": uid,
		"ukey": ukey,
	}

	resp = make_response(render_template("new.html", **content))

	expires = datetime.datetime.now() + datetime.timedelta(days=180)
	resp.set_cookie("uid", uid, expires=expires, samesite="strict", domain=".leprechaunb.com")

	expires = datetime.datetime.now() + datetime.timedelta(days=28)
	resp.set_cookie("ukey_token", ukey_token, expires=expires, samesite="strict", domain=".leprechaunb.com")

	return resp


@login_blueprint.route("/login/logout/", methods=["GET"])
def login_logout():

	resp = make_response(redirect("/", code=302))

	resp.set_cookie("uid", "", expires=0, samesite="strict", domain=".leprechaunb.com")
	resp.set_cookie("ukey_token", "", expires=0, samesite="strict", domain=".leprechaunb.com")

	return resp


