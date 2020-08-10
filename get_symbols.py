#!/usr/bin/python3
from custom_log import Custom_Logger
import requests
import json

logger = Custom_Logger().write_log

class Get_symbols():
  def get_data(self,url):
    symbols = []
    r = requests.get(url)
    data = r.text
    for line in data.splitlines():
      if 'ASXL' not in url:
        symbol = line.split(',')[0].strip('"')
        if '^' in symbol:
          symbol = symbol.split('^')[0]
        if '.' in symbol:
          symbol = symbol.split('.')[0]
        symbol = symbol.strip()
        symbols.append(symbol)
      else:
        if line.startswith('"'):
          symbol = line.split(',')[1].strip('"')
          if '^' in symbol:
            symbol = symbol.split('^')[0]
          if '.' in symbol:
            symbol = symbol.split('.')[0]
          symbol = symbol.strip()
          symbols.append(symbol)
    return symbols

  def get_symbols(self):
    nasdaq = 'https://old.nasdaq.com/screening/companies-by-name.aspx?letter=0&exchange=nasdaq&render=download'
    nyse = 'https://old.nasdaq.com/screening/companies-by-name.aspx?letter=0&exchange=amex&render=download'
    asxl = 'https://old.nasdaq.com/screening/companies-by-name.aspx?letter=0&exchange=nyse&render=download'
    all = []
    all = all + self.get_data(nasdaq)
    all = all + self.get_data(nyse)
    all = all + self.get_data(asxl)
    all = list(set(all))
    return sorted(all)
