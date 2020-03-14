"""
Generic key history.
"""
from datetime import datetime, timedelta

import pandas as pd

from util import logger
from util import racoon
from util import rock


tsdb_keys = list(rock.rocks("tsdbrocks").get("tsdb_data").keys())


def minute_arrow():
	"""
	Maintain the minutely key files.
	"""
	logger.info("<keys_minutely>")
	for key in tsdb_keys:
		if key.endswith("_timestamp"):
			continue
		df = pd.read_parquet(f"/data/tsdb/minutely/{key}.parq")
		date_filter = datetime.utcnow().date() - timedelta(days=7*4)
		df = df.query(f"date > '{date_filter}'")
		df = df.dropna()
		racoon.to_csv(df, f"/data/adbcsv/{key}_minutely.csv")
	logger.info("</keys_minutely>")



