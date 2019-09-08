#!/usr/bin/env python3
"""
Currency crisis center.
"""
import time
import schedule
from multiprocessing import Process

from util import logger
import price_history


def minute_arrow():
	try:
		p = Process(target=price_history.arrow)
		p.start()
		p.join()
	except Exception as ex:
		logger.exception(ex, "Root minute_arrow exception handler:")
		time.sleep(4)

schedule.every(10).seconds.do(minute_arrow)


while True:
    schedule.run_pending()
    time.sleep(1)
