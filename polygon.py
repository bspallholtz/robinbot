#!/usr/bin/python
#import os
#import alpaca_trade_api
import requests
import json
#api = alpaca_trade_api.REST(os.environ['APCA_API_KEY_ID'], os.environ['APCA_API_SECRET_KEY'], os.environ['APCA_API_BASE_URL'])


#get_data() must be called with Alpaca instance
class Alpaca:
  def get_symbols(self):
    symbols = []
    end = "https://api.polygon.io/v2/snapshot/locale/us/markets/stocks/tickers?apiKey=AKCW3CLVYM42U0ZYM90B"
    r = requests.get(end)
    if r.status_code != 200:
      return False
    data = json.loads(r.text)
    data = data['tickers']
    for ticker in data:
      symbols.append(ticker['ticker'])
    return symbols

  def find_symbol(self, symbol):
    end = "https://api.polygon.io/v2/reference/tickers?apiKey=AKCW3CLVYM42U0ZYM90B&search=%s" % symbol
    r = requests.get(end)
    data = json.loads(r.text)
    return data

  def alpaca_check(self, symbol):
    end = "https://api.polygon.io/v1/meta/symbols/%s/analysts?apiKey=AKCW3CLVYM42U0ZYM90B" % symbol
    r = requests.get(end)
    if r.status_code != 200:
      print("ALPACA %s unable to get data" % symbol)
      return False
    data = json.loads(r.text)
    if 'analysts' not in data.keys():
      print("ALPACA %s analysts not found" % symbol)
      return False
    if int(data['analysts']) <= 5:
      print("ALPACA %s not enought analysts" % symbol)
      return False
    if 'mean' not in data.keys():
      print("ALPACA %s no mean analysts" % symbol)
      return False
    if 'current' not in data['mean'].keys():
      print("ALPACA %s no current analysts" % symbol)
      return False
    mean = data['mean']['current']
    if float(mean) <= 1.5:
      print("ALPACA %s is a buy" % symbol)
      return True
    else:
      print("ALPACA %s not a buy" % symbol)
      return False
