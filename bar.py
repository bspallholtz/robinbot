#!/usr/bin/python3
from finviz import FinViz
from barchart import Barchart
import robin_stocks

analysts = 10
symbols = FinViz().full()
buys = []
for symbol in symbols:
    if Barchart().analysts(symbol, analysts) is True and robin_hood_analysts(symbol, analysts) is True:
        buys.append(symbol)
        if buy(symbol) is True:
            track_buys().buy(symbol, cp, True)

for symbol in tack_buys().get_symbols():
    if symbol not in buys:
        track_buys().buy(symbol, get_cp(symbol), False)

