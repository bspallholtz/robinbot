#!/usr/bin/python3
import yfinance as yf
import statistics
import json

class Find_SLP():
  def get_slp(self, symbol):
    symbol_data = yf.Ticker(symbol)
    hist = symbol_data.history(period="1y")
    result = hist.to_json(orient="split")
    result = json.loads(result)
    changes = []
    for index, row  in enumerate(result['data']):
         if index < 3 or index >= 250:
             continue
         highs_lows = []
         highs_lows.append(row[1])
         highs_lows.append(row[2])
         highs_lows.append(result['data'][index - 1][1])
         highs_lows.append(result['data'][index - 2][1])
         highs_lows.append(result['data'][index - 1][2])
         highs_lows.append(result['data'][index - 2][2])
         highs_lows.append(result['data'][index + 1][1])
         highs_lows.append(result['data'][index + 2][1])
         highs_lows.append(result['data'][index + 1][2])
         highs_lows.append(result['data'][index + 2][2])
         high = max(highs_lows)
         low = min(highs_lows)
         diff = abs(high - low)
         change = ( diff / high ) * 100
         changes.append(change)
    res = statistics.pstdev(changes)
    mean = statistics.mean(changes)
    slp = (res + mean) * -1
    return slp

