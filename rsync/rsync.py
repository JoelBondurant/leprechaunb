#!/usr/bin/env python3
"""
Rsync backup.
"""

import importlib
import os
import subprocess as sp
import time

import schedule

from util import logger


ts_bak_idx = 0
def ts_rsync():
	"""
	ts rsync backup
	"""
	global ts_bak_idx
	logger.info(f"<ts_rsync bak_idx={ts_bak_idx}>")
	src_path = "/data/tsdb/"
	bak_path = f"/data/bak/tsdb/{ts_bak_idx}/"
	os.makedirs(bak_path, mode=0o770, exist_ok=True)
	sp.call(["rsync", "-r", src_path, bak_path])
	zorder = 3
	if ts_bak_idx == 0:
		logger.info(f"<ts_rsync backblaze>")
		sp.call(["b2", "sync", "/data/bak/tsdb", "b2://leprechaunbak/tsdb"])
		logger.info(f"</ts_rsync backblaze>")
	ts_bak_idx = (ts_bak_idx + 1) % zorder
	logger.info(f"</ts_rsync>")


sqlite_bak_idx = 0
def sqlite_rsync():
	"""
	sqlite rsync backup
	"""
	global sqlite_bak_idx
	logger.info(f"<sqlite_rsync bak_idx={sqlite_bak_idx}>")
	src_path = "/data/sqlite/"
	bak_path = f"/data/bak/sqlite/{sqlite_bak_idx}/"
	os.makedirs(bak_path, mode=0o770, exist_ok=True)
	sp.call(["rsync", "-r", src_path, bak_path])
	zorder = 3
	if sqlite_bak_idx == 0:
		logger.info(f"<sqlite_rsync backblaze>")
		sp.call(["b2", "sync", "/data/bak/sqlite", "b2://leprechaunbak/sqlite"])
		logger.info(f"</sqlite_rsync backblaze>")
	sqlite_bak_idx = (sqlite_bak_idx + 1) % zorder
	logger.info(f"</sqlite_rsync>")


def main():
	"""
	Main rsync entry point.
	"""
	logger.warn("leprechaun rsync started.")

	time.sleep(1)
	ts_rsync()
	sqlite_rsync()

	while True:
		try:
			# schedule crash guard:
			importlib.reload(schedule)
			schedule.every(1301).seconds.do(ts_rsync)
			schedule.every(300).seconds.do(sqlite_rsync)
			while True:
				try:
					time.sleep(2)
					schedule.run_pending()
				except Exception as ex:
					logger.exception(ex)
					time.sleep(2)
		except Exception as ex:
			logger.exception(ex)
			time.sleep(2)


if __name__ == "__main__":
	main()

