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


pot_blueprint = Blueprint("pot", __name__)



def sort_pot(apot):
	if apot is None:
		return None
	for idx in range(len(apot)):
		apot[idx]["id"] = idx
	apot = sorted(apot, key=lambda x: (x["datebin"], x["id"]))
	for idx in range(len(apot)):
		apot[idx]["id"] = idx
	return list(apot)


@pot_blueprint.route("/pot/", methods=["GET"])
def pot():
	if not auth.is_verified():
		return auth.unverified_redirect()

	content = {}

	uid = request.cookies.get("uid")

	udb = sqlite.KV("udb")
	pot_gold = udb.get(f"pot_gold_{uid}")
	pot_gold = auth.lt_decrypt(pot_gold)
	if pot_gold is None or pot_gold == "":
		pot_gold = []
	else:
		pot_gold = json.loads(pot_gold)
	content["pot_gold"] = pot_gold

	pot_bitcoin = udb.get(f"pot_bitcoin_{uid}")
	pot_bitcoin = auth.lt_decrypt(pot_bitcoin)
	if pot_bitcoin is None or pot_bitcoin == "":
		pot_bitcoin = []
	else:
		pot_bitcoin = json.loads(pot_bitcoin)
	content["pot_bitcoin"] = pot_bitcoin

	return make_response(render_template("pot.html", **content))


@pot_blueprint.route("/pot/gold/", methods=["GET", "POST"])
def gold():
	return auth.verified_response("pot_gold.html")


@pot_blueprint.route("/pot/gold/new", methods=["POST"])
def new_gold():
	if not auth.is_verified():
		return auth.unverified_redirect()

	uid = request.cookies.get("uid")

	datebin = request.form.get("datebin")
	grams = request.form.get("grams")
	source = request.form.get("source")
	latitude = request.form.get("latitude")
	longitude = request.form.get("longitude")
	cost_usd = request.form.get("cost_usd")
	local_key = request.form.get("local_key")
	note = request.form.get("note")

	udb = sqlite.KV("udb")
	key = f"pot_gold_{uid}"
	pot_json = udb.get(key)
	if pot_json is None:
		gold_pot = []
	else:
		pot_json = auth.lt_decrypt(pot_json)
		gold_pot = json.loads(pot_json)
	gold_pot += [
		{
			"datebin": datebin,
			"grams": grams,
			"source": source,
			"latitude": latitude,
			"longitude": longitude,
			"cost_usd": cost_usd,
			"local_key": local_key,
			"note": note,
		}
	]
	gold_pot = sort_pot(gold_pot)
	pot_json = json.dumps(gold_pot)
	pot_json = auth.lt_encrypt(pot_json)
	udb.put(key, pot_json)

	resp = make_response(redirect("/pot", code=302))
	return resp


@pot_blueprint.route("/pot/bitcoin/", methods=["GET", "POST"])
def bitcoin():
	return auth.verified_response("pot_bitcoin.html")


@pot_blueprint.route("/pot/bitcoin/new", methods=["POST"])
def new_bitcoin():
	if not auth.is_verified():
		return auth.unverified_redirect()

	uid = request.cookies.get("uid")

	datebin = request.form.get("datebin")
	sats = request.form.get("sats")
	source = request.form.get("source")
	pub_key = request.form.get("pub_key")
	priv_key = request.form.get("priv_key")
	cost_usd = request.form.get("cost_usd")
	local_key = request.form.get("local_key")
	note = request.form.get("note")

	udb = sqlite.KV("udb")
	key = f"pot_bitcoin_{uid}"
	pot_json = udb.get(key)
	if pot_json is None:
		bitcoin_pot = []
	else:
		pot_json = auth.lt_decrypt(pot_json)
		bitcoin_pot = json.loads(pot_json)
	bitcoin_pot += [
		{
			"datebin": datebin,
			"sats": sats,
			"source": source,
			"pub_key": pub_key,
			"priv_key": priv_key,
			"cost_usd": cost_usd,
			"local_key": local_key,
			"note": note,
		}
	]
	bitcoin_pot = sort_pot(bitcoin_pot)
	pot_json = json.dumps(bitcoin_pot)
	pot_json = auth.lt_encrypt(pot_json)
	udb.put(key, pot_json)

	resp = make_response(redirect("/pot", code=302))
	return resp

