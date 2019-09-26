#!/usr/bin/env python3
"""
Currency crisis center.
"""
import importlib
import time

import schedule

from util import logger
from util import rock

import spot_history



def rt_arrow():
	try:
		logger.info("<rt_arrow>")
		rtdb_data = rock.rocks("tsdbrocks").get("rtdb_data")
		rtdb_data["adb_timestamp"] = int(time.time())
		rock.rocks("adbrocks").put("rtdb_data", rtdb_data)
		logger.info("</rt_arrow>")
	except Exception as ex:
		logger.exception(ex, "Root rt_arrow exception handler:")
		time.sleep(2)


def minute_arrow():
	try:
		logger.info("<minute_arrow>")
		importlib.reload(spot_history)
		spot_history.minute_arrow()
		logger.info("</minute_arrow>")
	except Exception as ex:
		logger.exception(ex, "Root minute_arrow exception handler:")
		time.sleep(2)


def day_arrow():
	try:
		logger.info("<day_arrow>")
		spot_history.day_arrow()
		logger.info("</day_arrow>")
	except Exception as ex:
		logger.exception(ex, "Root day_arrow exception handler:")
		time.sleep(2)


def main():
	"""
	Main entry to arrows.
	"""
	logger.info("arrows started.")

	time.sleep(1)
	rt_arrow()
	minute_arrow()
	day_arrow()

	while True:
		try:
			# schedule crash guard.
			importlib.reload(schedule)
			schedule.every(10).seconds.do(rt_arrow)
			schedule.every(20).seconds.do(minute_arrow)
			schedule.every(120).seconds.do(day_arrow)
			while True:
				try:
					time.sleep(1)
					schedule.run_pending()
				except Exception as ex:
					logger.exception(ex, "Arrows schedule.run_pending exception handler:")
					time.sleep(2)
		except Exception as ex:
			logger.exception(ex, "Root arrows exception handler:")
			time.sleep(2)



if __name__ == "__main__":
	main()

