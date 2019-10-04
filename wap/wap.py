#!/usr/bin/env python3
import datetime
import json
import logging
import os
import time
import uuid

import cachetools.func

from flask import (
	Flask,
	make_response,
	redirect,
	render_template,
	request,
	send_from_directory,
)
from flask.logging import default_handler

from views.index import index_blueprint

from util import rock


COOKIES = True

this_path = os.path.dirname(os.path.realpath(__file__))
os.chdir(this_path)


app = Flask("leprechaunb", static_url_path="", template_folder="rws")
app.register_blueprint(index_blueprint)
gunicorn_logger = logging.getLogger("gunicorn.error")
app.logger.handlers = gunicorn_logger.handlers
app.logger.setLevel(gunicorn_logger.level)



@app.template_filter("strtime")
def strtime(s):
	return datetime.datetime.fromtimestamp(s).isoformat().replace("T","_")


@app.errorhandler(404)
def awol(err):
	return render_template("404.html"), 404


@app.route("/exchange")
def exchange():
	return render_template("exchange.html")


@app.route("/alert")
def alert():
	return render_template("alert.html")


@app.route("/drill")
def drill():
	return render_template("drill.html")


@app.route("/pot")
def pot():
	return render_template("pot.html")


@app.route("/contact")
def contact():
	if "message" in request.args:
		ts = datetime.datetime.now().isoformat()
		msg = f"Message:{ts}:\n"
		msg += request.args.get("message")[:10000]
		with open("/data/messages/msg.txt", "a") as fout:
			fout.write(msg + "\n\n")
		time.sleep(1)
		return redirect(request.path, code=302)
	return render_template("contact.html")


@app.route("/about")
def about():
	return render_template("about.html")


@app.route("/favicon.ico")
def favicon():
	return send_from_directory("ws/img", "favicon.ico", mimetype="image/vnd.microsoft.icon")


@app.route("/ws/js/<file_name>")
def js(file_name):
	"""
	web site resources (js/css/etc) loader.
	file_name - the filename to load.
	"""
	return send_from_directory("ws/js", file_name)


@app.route("/ws/css/<file_name>")
def css(file_name):
	"""
	web site resources (js/css/etc) loader.
	file_name - the filename to load.
	"""
	return send_from_directory("ws/css", file_name)


@app.route("/ws/img/<file_name>")
def img(file_name):
	"""
	web site resources (js/css/etc) loader.
	file_name - the filename to load.
	"""
	return send_from_directory("ws/img", file_name)


@app.route("/arrows/<arrow_name>")
def arrow(arrow_name):
	"""
	arrow loader (png/html).
	arrow_name - the filename to load.
	"""
	if arrow_name.endswith(".csv"):
		return send_from_directory("/data/adbcsv", arrow_name)
	else:
		return render_template("404.html"), 404


@app.after_request
def add_header(response):
	"""
	Cache middleware for nginx.
	"""
	response.headers["Cache-Control"] = "public, min-fresh=12, max-age=1200"
	response.headers["Expires"] = "12"
	response.headers["Pragma"] = "no-cache"
	return response


