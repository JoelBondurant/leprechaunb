"""
Bitcoin sources covering.
"""

# Metadata:
from . import blockchain

# Spots:
from . import binance
from . import bisq
from . import bitfinex
from . import bitstamp
from . import bittrex
from . import btse
from . import cex
from . import coinbase
from . import gemini
from . import huobi
from . import itbit
from . import kraken
from . import poloniex


spot_sources = {
	"binance": binance,
	"bisq": bisq,
	"bitfinex": bitfinex,
	"bitstamp": bitstamp,
	"bittrex": bittrex,
	"btse": btse,
	"cex": cex,
	"coinbase": coinbase,
	"gemini": gemini,
	"huobi": huobi,
	"itbit": itbit,
	"kraken": kraken,
	"poloniex": poloniex,
}

spot_source_names =  list(spot_sources.keys())
spot_source_modules = list(spot_sources.values())

