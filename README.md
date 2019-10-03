# [leprechaunb.com](https://leprechaunb.com)

A system for monitoring Bitcoin.


## ScreenShot:
![ScreenShot](https://raw.github.com/JoelBondurant/leprechaunb/master/doc/img/leprechaunb.png)

## Architecture:
![Architechure](https://raw.github.com/JoelBondurant/leprechaunb/master/doc/img/arch.jpg)

1. rt - Real Time data collector service. (polling ~10 seconds)
1. rtdb - /data/rtdb/ (based on leveldb used by Bitcoin for fun)
1. ts - Time series builder service.
1. tsdb - /data/tsdb/*.parq, /data/tsdbrocks/
1. arrows - Arrows on tsdb.
1. adb - /data/adbcsv/*.csv, /data/adbrocks/
1. wap - A Flask app Bitcoin dashboard made with vega-lite.
1. nginx - cache, proxy to deprivilege, ssl automation...

