#!/usr/bin/env python3
import datetime
import json
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

from util import logger
from util import rock


COOKIES = True

logger.addHandler(default_handler)
logger.info("wap started.")
app = Flask("bitcoinarrows", static_url_path="", template_folder="rws")


@app.template_filter("strtime")
def strtime(s):
	return datetime.datetime.fromtimestamp(s).isoformat().replace("T","_")


@app.errorhandler(404)
def awol(err):
	return render_template("404.html"), 404


def gendeviceid():
	return str(uuid.uuid4())


def to_table(adict, table_id=None):
	if table_id:
		res = f'<table id="{table_id}">'
	else:
		res = "<table>"
	res += "<tr>"
	for key in adict.keys():
		res += f"<th>{key}</th>"
	res += "</tr><tr>"
	for val in adict.values():
		res += f"<td>{val}</td>"
	res += "</tr></table>"
	return res


@cachetools.func.ttl_cache(ttl=10)
def get_rtdb_data():
	"""
	Rate limit the hit squad.
	"""
	rtdb_data = rock.rocks("adbrocks").get("rtdb_data")
	return rtdb_data


@app.route("/")
def index():
	"""
	https://bitcoinarrows.com
	"""

	content = {}

	# RT Data:
	rtdb_data = get_rtdb_data()
	content.update(rtdb_data)

	stats = rtdb_data["blockchain_stats"]
	keep_stats = ["trade_volume_btc", "blocks_size", "hash_rate", "difficulty", "miners_revenue_btc", "n_blocks_total", "minutes_between_blocks"]
	stats = {k: stats[k] for k in keep_stats}
	stats = to_table(stats, table_id="stats")
	content["stats"] = stats
	#app.logger.info("content:" + str(content))

	# Time windowing for charts, this should go in some vega json format:
	now = datetime.datetime.now().replace(second=0, microsecond=0)
	hours_back = 1
	scroller_start = (now + datetime.timedelta(minutes=-hours_back*60)).isoformat()
	scroller_end = (now + datetime.timedelta(minutes=1)).isoformat()
	multiscroller_start = (now + datetime.timedelta(minutes=-hours_back*60)).isoformat()
	multiscroller_end = (now + datetime.timedelta(minutes=1)).isoformat()

	content.update({
		"scroller_start": scroller_start,
		"scroller_end": scroller_end,
		"multiscroller_start": multiscroller_start,
		"multiscroller_end": multiscroller_end,
	})

	resp = make_response(render_template("index.html", **content))
	
	if COOKIES:
		if "deviceid" not in request.cookies:
			deviceid = gendeviceid()
			expires = datetime.datetime.now() + datetime.timedelta(days=360)
			resp.set_cookie("deviceid", deviceid, expires=expires)

	return resp


@app.route("/exchange")
def exchange():
	return render_template("exchange.html")


@app.route("/drill")
def drill():
	return render_template("drill.html")


@app.route("/wallet")
def wallet():
	return render_template("wallet.html")


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
	response.headers["Cache-Control"] = "public, min-fresh=10, max-age=3600"
	response.headers["Pragma"] = "no-cache"
	response.headers["Expires"] = "10"
	return response



