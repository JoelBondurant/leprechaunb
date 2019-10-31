#!/usr/bin/env python3
import datetime
import json
import secrets
import time

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
from util import htm
from util import logger
from util import rock


logger.warn("wap started.")
index_blueprint = Blueprint("index", __name__)


@cachetools.func.ttl_cache(ttl=10)
def get_adb_data():
	"""
	Rate limit the hit squad.
	"""
	adb_rocks = rock.rocks("adbrocks", read_only=True)
	adb_data = adb_rocks.get("adb_data")
	adb_data["color_index"] = adb_rocks.get("color_index")
	return adb_data


@index_blueprint.route("/")
def index():
	"""
	https://leprechaunb.com
	"""
	content = {}

	rainbow = ["#80a", "#48f", "#0f0", "#ff0", "#f7931a", "#f00"]
	content["rainbow"] = rainbow

	content["login_link"] = "<a href='/login'>login</a>"
	if "uid" in request.cookies and "ukey_token" in request.cookies:
		uid = request.cookies.get("uid")
		ukey_token = request.cookies.get("ukey_token")
		if auth.verify_ukey_token(uid, ukey_token):
			content["login_link"] = "<a href='/login/logout'>logout</a>"

	# Arrows Data:
	adb_data = get_adb_data()
	content.update(adb_data)

	# Unroll blockchain stats
	stats = {}
	color_index = adb_data["color_index"] + 1
	stats["color_index"] = color_index
	spot_color = rainbow[color_index - 1]
	content["spot_color"] = spot_color
	bstats = adb_data["blockchain_stats"]
	keep_bstats = ["trade_volume_btc", "blocks_size", "hash_rate", "difficulty", "miners_revenue_btc", "n_blocks_total", "minutes_between_blocks"]
	bstats = {k: bstats[k] for k in keep_bstats}
	stats.update(bstats)
	stats = htm.to_table(stats, table_id="stats")
	tdx = stats.find("td")
	stats = stats[:tdx + 2] + f' style="color:{spot_color};"' + stats[tdx + 2:]
	content["stats"] = stats
	#index_blueprint.logger.info("content:" + str(content))

	# Time windowing for charts, this should go in some vega json format:
	now = datetime.datetime.now().replace(second=0, microsecond=0)
	hours_back = 48
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
	
	if "deviceid" not in request.cookies or len(request.cookies.get("deviceid")) != 32:
		deviceid = secrets.token_hex(16)
		expires = datetime.datetime.now() + datetime.timedelta(days=180)
		resp.set_cookie("deviceid", deviceid, expires=expires, samesite="strict", domain=".leprechaunb.com")
		current_app.logger.info(f"new:deviceid:{deviceid}")
	else:
		deviceid = request.cookies.get("deviceid")
		current_app.logger.info(f"deviceid:{deviceid}")

	return resp

