#!/usr/bin/env python3

import json


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


from util import auth
from util import sqlite


pot_blueprint = Blueprint("pot", __name__)


@pot_blueprint.route("/pot/", methods=["GET"])
def pot():

	content = {}

	if ("uid" not in request.cookies) or ("ukey_token" not in request.cookies):
		return make_response(redirect("/login", code=302))

	uid = request.cookies.get("uid")
	ukey_token = request.cookies.get("ukey_token")

	if not auth.verify_ukey_token(uid, ukey_token):
		return make_response(redirect("/login", code=302))

	pdat = sqlite.KV("udb").get(f"pot_{uid}")
	if pdat is None or pdat == "":
		pdat = {}
	else:
		pdat = auth.lt_decrypt(pdat)
		pdat = json.loads(pdat)
	content["pdat"] = pdat

	return make_response(render_template("pot.html", **content))


@pot_blueprint.route("/pot/gold/", methods=["GET", "POST"])
def gold():

	content = {}

	if ("uid" not in request.cookies) or ("ukey_token" not in request.cookies):
		return make_response(redirect("/login", code=302))

	uid = request.cookies.get("uid")
	ukey_token = request.cookies.get("ukey_token")

	if not auth.verify_ukey_token(uid, ukey_token):
		return make_response(redirect("/login", code=302))

	return make_response(render_template("pot_gold.html", **content))


@pot_blueprint.route("/pot/gold/new", methods=["POST"])
def new_gold():

	if ("uid" not in request.cookies) or ("ukey_token" not in request.cookies):
		return make_response(redirect("/login", code=302))

	uid = request.cookies.get("uid")
	assert len(uid) == 16
	ukey_token = request.cookies.get("ukey_token")

	if not auth.verify_ukey_token(uid, ukey_token):
		return make_response(redirect("/login", code=302))

	datebin = request.form.get("datebin")
	grams = request.form.get("grams")
	source = request.form.get("source")
	latitude = request.form.get("latitude")
	longitude = request.form.get("longitude")
	note = request.form.get("note")

	udb = sqlite.KV("udb")
	key = f"pot_gold_{uid}"
	pot_json = udb.get(key)
	if pot_json is None:
		pot = []
	else:
		pot_json = auth.lt_decrypt(pot_json)
		pot = json.loads(pot_json)
	pot += [
		{
			"datebin": datebin,
			"grams": grams,
			"source": source,
			"latitude": latitude,
			"longitude": longitude,
			"note": note,
		}
	]
	pot_json = json.dumps(pot)
	pot_json = auth.lt_encrypt(pot_json)
	udb.put(key, pot_json)

	resp = make_response(redirect("/pot", code=302))
	return resp


@pot_blueprint.route("/pot/bitcoin/", methods=["GET", "POST"])
def bitcoin():

	content = {}

	if ("uid" not in request.cookies) or ("ukey_token" not in request.cookies):
		return make_response(redirect("/login", code=302))

	uid = request.cookies.get("uid")
	ukey_token = request.cookies.get("ukey_token")

	if not auth.verify_ukey_token(uid, ukey_token):
		return make_response(redirect("/login", code=302))

	return make_response(render_template("pot_bitcoin.html", **content))


@pot_blueprint.route("/pot/bitcoin/new", methods=["POST"])
def new_bitcoin():

	if ("uid" not in request.cookies) or ("ukey_token" not in request.cookies):
		return make_response(redirect("/login", code=302))

	uid = request.cookies.get("uid")
	assert len(uid) == 16
	ukey_token = request.cookies.get("ukey_token")

	if not auth.verify_ukey_token(uid, ukey_token):
		return make_response(redirect("/login", code=302))

	datebin = request.form.get("datebin")
	sats = request.form.get("sats")
	source = request.form.get("source")
	pub_key = request.form.get("pub_key")
	priv_key = request.form.get("priv_key")
	note = request.form.get("note")

	udb = sqlite.KV("udb")
	key = f"pot_bitcoin_{uid}"
	pot_json = udb.get(key)
	if pot_json is None:
		pot = []
	else:
		pot_json = auth.lt_decrypt(pot_json)
		pot = json.loads(pot_json)
	pot += [
		{
			"datebin": datebin,
			"sats": sats,
			"source": source,
			"pub_key": pub_key,
			"priv_key": priv_key,
			"note": note,
		}
	]
	pot_json = json.dumps(pot)
	pot_json = auth.lt_encrypt(pot_json)
	udb.put(key, pot_json)

	resp = make_response(redirect("/pot", code=302))
	return resp

