#!/usr/bin/python3
import requests
from bs4 import BeautifulSoup

class Barchart:
  def analysts(self, symbol,analysts):
    end = "https://www.barchart.com/stocks/quotes/%s/analyst-ratings" % symbol
    r = requests.get(end, headers={'User-Agent': 'curl/7.61.1','Accept': '*/*'})
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
    analysts_recommendation = float(str(data[0]).split('>')[1].split('<')[0])
    number_of_analysts = float(str(data[1]).split('>')[2].split('<')[0])
    if analysts_recommendation > 4 and number_of_analysts > analysts:
      return True
    else:
      return False

