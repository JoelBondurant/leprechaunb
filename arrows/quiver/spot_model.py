"""
Bitcoin rainbow model.
"""

import numpy as np
import pandas as pd

from util import logger
from util import racoon
from util import rock
from util import stats


def day_arrow():
	"""
	Daily spot model.
	"""
	logger.info("<day_spot_model>")

	fn = "/data/tsdb/daily/spot_xaubtc.parq"
	df = pd.read_parquet(fn)
	df.columns = ["date", "spot"]

	df["time"] = range(len(df))
	df["log1p_spot"] = df.spot.apply(np.log1p)

	aa, bb, cc, dd, ee = np.polyfit(df.time, df.log1p_spot, 4)

	labels = [f"spot_model_{x}" for x in range(6)]
	#log_pads = [-0.80, -0.40, 0.0, 0.5, 1, 1.2]
	#exp_pads = [0.662, 0.496, 0.248, -0.244, -1.044, -1.512]
	log_pads = [-0.80, -0.40, 0.0, 0.5, 1.0, 1.1]
	exp_pads = [0.66, 0.5, 0.25, -0.2, -1.0, -1.1]
	#log_pads = [0, 0, 0, 0, 0, 0]
	#exp_pads = [0, 0, 0, 0, 0, 0]
	for label, lpad, epad in zip(labels, log_pads, exp_pads):
		log1p_spot_model = aa*df.time**4 + bb*df.time**3 + cc*df.time**2 + dd*df.time + ee
		log1p_spot_model += lpad
		spot_model = np.exp(log1p_spot_model) - 1
		spot_model += epad
		df[f"{label}"] = spot_model
		df[f"{label}"] = df[f"{label}"].apply(lambda x: max(x, 0.01))


	spot_model_bands = df[labels].tail(1).values.tolist()[0]
	spot = df.spot.iloc[-1]
	spot_model_band = stats.closest(spot_model_bands, spot)
	color_index = spot_model_bands.index(spot_model_band)

	rock.rocks("adbrocks").put("spot_model_bands", spot_model_bands)
	rock.rocks("adbrocks").put("color_index", color_index)

	racoon.to_csv(df, "/data/adbcsv/spot_model_xaubtc_daily.csv")
	logger.info("</day_spot_model>")

