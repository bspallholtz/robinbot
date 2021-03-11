#!/usr/bin/python3.7
import yfinance as yf
import json
import pandas
from random import randrange
from work_sql import database
from custom_log import Custom_Logger
import time


log = Custom_Logger().write_log

database()

def calculate_profit():
    database().clear_profits()
    symbols = database().get_symbols()
    for symbol in symbols:
        transactions = database().get_transactions(symbol)
        if database().detect_state(symbol) == 'open':
            transactions = transactions[:-1]
        if transactions[0][2] != 'BUY':
          log('ERROR', 'Something wrong with the transaction order, breaking')
          exit(1)
        for index, transaction in enumerate(transactions):
            if transaction[2] == 'SELL':
                continue
            buy_price = transaction[3] * -1
            buy_date = transaction[4]
            sell_price = transactions[index + 1][3]
            sell_date = transactions[index + 1][4]
            profit = buy_price + sell_price
            database().write_profit(symbol,buy_price,buy_date,sell_price,sell_date,profit)
    


symbol = 'AAPL'
data = yf.Ticker(symbol)
data = data.history(period="1y")
data = data.to_json(orient="split")
data = json.loads(data)
#Open","High","Low","Close","Volume","Dividends","Stock Splits"
data = data['data']
for day in data:
    price = float(day[2])
    if randrange(100) <= 12:
        log('INFO', 'Attempting a buy')
        if database().detect_state('AAPL') == 'closed':
            log('INFO', 'Position is closed, executing a buy')
            log('INFO', str(database().execute('AAPL', 'BUY', price)))
        else:
            log('INFO', 'Position is open, not buying')
    if randrange(100) <= 6:
        log('INFO', 'Attempting a sell')
        if database().detect_state('AAPL') == 'open':
            log('INFO', 'Position is open, going to execute a sell')
            log('INFO', str(database().execute('AAPL', 'SELL', price)))
        else:
            log('INFO', 'Position is close, not selling')
    time.sleep(1)

calculate_profit()

