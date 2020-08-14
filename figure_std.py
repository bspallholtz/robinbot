#!/usr/bin/python3
import yfinance as yf
import statistics
import json


msft = yf.Ticker("IOVA")


hist = msft.history(period="1y")
result = hist.to_json(orient="split")
result = json.loads(result)
#["Open","High","Low","Close","Volume","Dividends","Stock Splits"]
changes = []
for index, row  in enumerate(result['data']):
     if index < 2 or index > 250:
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
     print("The high for MSFT was %f and the low was %f and the diff was %f the percentage swings was %f" % ( high, low, diff, change))


res = statistics.pstdev(changes)
mean = statistics.mean(changes)
move = res + mean
print("The mean for the data set was %f" % mean )
print("The STD for the data set was %f" % res)
print("If the stock moves down by more than more than %f it is then outside one STD" % move)

#hist.pct_change().rolling(window_size).std()*(252**0.5)

