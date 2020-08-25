#!/usr/bin/python3
import requests
from bs4 import BeautifulSoup
from custom_log import Custom_Logger

class Barchart:
  def buy(self, symbol):
    end = "https://www.barchart.com/stocks/quotes/%s/analyst-ratings" % symbol
    r = requests.get(end, headers={'User-Agent': 'curl/7.61.1','Accept': '*/*'})
    #r = requests.get(end)
    if r.status_code != 200:
      return False
    data = r.text
    soup = BeautifulSoup(data, "html.parser")
    spans = soup.find_all('span')
    data = []
    for index, span in enumerate(spans):
      if span.string == 'Current':
        spot = index + 1
        foo = spans[spot]
        data.append(foo)
    if len(data) == 0:
      return False
    ar = float(str(data[0]).split('>')[1].split('<')[0])
    an = float(str(data[1]).split('>')[2].split('<')[0])
    if ar > 4 and an > 5:
      return True
    else:
      return False

