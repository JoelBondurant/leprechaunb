"""
Gold sources covering.
"""

from . import apmex
from . import freeforexapi
from . import jmbullion
from . import kitco
from . import lbma


spot_sources = {
	"apmex": apmex,
	"freeforexapi": freeforexapi,
	"jmbullion": jmbullion,
	"kitco": kitco,
	"lbma": lbma
}

spot_source_names =  list(spot_sources.keys())
spot_source_modules = list(spot_sources.values())

