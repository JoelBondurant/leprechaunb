#!/usr/bin/env python3
import datetime
import json
import time
import uuid


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


def gendeviceid():
	return str(uuid.uuid4())


@login_blueprint.route("/login/")
def login():

	content = {}

	resp = make_response(render_template("login.html", **content))
	
	if "deviceid" not in request.cookies:
		deviceid = gendeviceid()
		expires = datetime.datetime.now() + datetime.timedelta(days=360)
		resp.set_cookie("deviceid", deviceid, expires=expires)
		current_app.logger.info(f"new:deviceid:{deviceid}")
	else:
		deviceid = request.cookies.get("deviceid")
		current_app.logger.info(f"deviceid:{deviceid}")

	return resp

