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


@app.errorhandler(404)
def awol(err):
	return render_template("404.html"), 404

def gendeviceid():
	return str(uuid.uuid4())

@app.route("/")
def index():
	spot = rtdb.get("spot")
	gold_spot = rtdb.get("gold_spot")
	binance_spot = rtdb.get("binance_spot")
	bitfinex_spot = rtdb.get("bitfinex_spot")
	bitstamp_spot = rtdb.get("bitstamp_spot")
	coinbase_spot = rtdb.get("coinbase_spot")
	kraken_spot = rtdb.get("kraken_spot")
	now = datetime.datetime.now().replace(second=0, microsecond=0)
	scroller_start = (now + datetime.timedelta(minutes=-72*60)).isoformat()
	scroller_end = (now + datetime.timedelta(minutes=61)).isoformat()
	multiscroller_start = (now + datetime.timedelta(minutes=-4*60)).isoformat()
	multiscroller_end = (now + datetime.timedelta(minutes=1)).isoformat()
	content = {
		"spot": spot,
		"gold_spot": gold_spot,
		"binance_spot": binance_spot,
		"bitfinex_spot": bitfinex_spot,
		"bitstamp_spot": bitstamp_spot,
		"coinbase_spot": coinbase_spot,
		"kraken_spot": kraken_spot,
		"scroller_start": scroller_start,
		"scroller_end": scroller_end,
		"multiscroller_start": multiscroller_start,
		"multiscroller_end": multiscroller_end,
	}
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


