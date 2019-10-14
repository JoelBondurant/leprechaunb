#!/usr/bin/env python3

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
from util import rock

pot_blueprint = Blueprint("pot", __name__)


@pot_blueprint.route("/pot/", methods=["GET"])
def pot():

	content = {}

	if "deviceid" not in request.cookies:
		current_app.logger.info(f"login:nocookies")
		return make_response(render_template("cookies.html", **content))

	deviceid = request.cookies.get("deviceid")
	if ("uid" not in request.cookies) or ("ukey_token" not in request.cookies):
		return make_response(redirect("/login", code=302))

	uid = request.cookies.get("uid")
	ukey_token = request.cookies.get("ukey_token")

	if not auth.verify_ukey_token(uid, ukey_token):
		return make_response(redirect("/login", code=302))

	return make_response(render_template("pot.html", **content))
