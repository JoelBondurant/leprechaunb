#!/usr/bin/env python3
import datetime
import json
import uuid

from flask import Flask, request, send_from_directory, render_template, make_response

from util import logger
from util import rock


COOKIES = True


logger.info("wap started.")
app = Flask("bitcoinarrows", static_url_path="", template_folder="rws")
app.config["SEND_FILE_MAX_AGE_DEFAULT"] = 1

rtdb = rock.Rock("rtdb")

sources = [
	# Bitcoin spots:
	"binance_spot",
	"bisq_spot",
	"bitfinex_spot",
	"bitstamp_spot",
	"bittrex_spot",
	"btse_spot",
	"cex_spot",
	"coinbase_spot",
	"gemini_spot",
	"huobi_spot",
	"itbit_spot",
	"kraken_spot",
	"poloniex_spot",
	# Gold spots:
	"apmex_spot",
	"gold_spot",
	# Bitcoin:
	"spot",
	"spot_usd"
]


@app.errorhandler(404)
def awol(err):
	return render_template("404.html"), 404

def gendeviceid():
	return str(uuid.uuid4())

@app.route("/")
def index():
	"""
	https://bitcoinarrows.com
	"""

	content = {}
	for source in sources:
		val = rtdb.get(source)
		content[source] = val

	# Time windowing for charts, this should go in some vega json format:
	now = datetime.datetime.now().replace(second=0, microsecond=0)
	scroller_start = (now + datetime.timedelta(minutes=-72*60)).isoformat()
	scroller_end = (now + datetime.timedelta(minutes=61)).isoformat()
	multiscroller_start = (now + datetime.timedelta(minutes=-1*60)).isoformat()
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


@app.route("/about")
def about():
	return render_template("about.html")


@app.route("/ws/<file_name>")
def ws(file_name):
	"""
	web site resources (js/css/etc) loader.
	file_name - the filename to load.
	"""
	return send_from_directory("ws", file_name)


@app.route("/arrows/<arrow_name>")
def arrow(arrow_name):
	"""
	arrow loader (png/html).
	arrow_name - the filename to load.
	"""
	return send_from_directory("/data/arrows", arrow_name)


@app.after_request
def add_header(response):
	response.headers["Cache-Control"] = "public, max-age=0"
	response.headers["Pragma"] = "no-cache"
	response.headers["Expires"] = "-1"
	return response


