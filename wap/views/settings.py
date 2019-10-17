#!/usr/bin/env python3

import json


import cachetools.func


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
from util import sqlite


settings_blueprint = Blueprint("settings", __name__)



@settings_blueprint.route("/settings/", methods=["GET", "POST"])
def get_settings():

	content = {}

	if ("uid" not in request.cookies) or ("ukey_token" not in request.cookies):
		return make_response(redirect("/login", code=302))

	uid = request.cookies.get("uid")
	ukey_token = request.cookies.get("ukey_token")

	if not auth.verify_ukey_token(uid, ukey_token):
		return make_response(redirect("/login", code=302))

	udb = sqlite.KV("udb")
	settings = udb.get(f"usettings_{uid}")
	settings = auth.lt_decrypt(settings)
	if settings is None or settings == "":
		settings = {}
	else:
		settings = json.loads(settings)
	content["settings"] = settings

	return make_response(render_template("settings.html", **content))


@settings_blueprint.route("/settings/sync", methods=["POST"])
def post_settings():

	if ("uid" not in request.cookies) or ("ukey_token" not in request.cookies):
		return make_response(redirect("/login", code=302))

	uid = request.cookies.get("uid")
	assert len(uid) == 16
	ukey_token = request.cookies.get("ukey_token")

	if not auth.verify_ukey_token(uid, ukey_token):
		return make_response(redirect("/login", code=302))

	email = request.form.get("email")
	benemail_date = request.form.get("benemail_date")
	benemails = request.form.get("benemails")
	benemail_delay = request.form.get("benemail_delay")
	note = request.form.get("note")

	settings = {
		"email": email,
		"benemail_date": benemail_date,
		"benemails": benemails,
		"benemail_delay": benemail_delay,
		"note": note,
	}

	settings_json = json.dumps(settings)
	sdat = auth.lt_encrypt(settings_json)

	udb = sqlite.KV("udb")
	key = f"usettings_{uid}"

	udb.put(key, sdat)

	resp = make_response(redirect("/settings", code=302))
	return resp

