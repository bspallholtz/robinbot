#!/usr/bin/python3
from get_symbols import Get_symbols
from cnn_money import Money

symbols = Get_symbols().get_symbols()
for symbol in symbols:
    if Money().get_data(symbol) is True:
        print(symbol)
