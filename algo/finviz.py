#!/usr/bin/python3
# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup

class FinViz():
    def get_an_recom(self, an_recom=None):
        possible = [ 'strongbuy', 'buybetter', 'buy' ]
        if an_recom is None:
            an_recom = 'strongbuy'
        if isinstance(an_recom, str) is False:
            an_recom = 'strongbuy'
        if an_recom not in possible:
            an_recom = 'strongbuy'
        return an_recom

    def get_cap(self, cap=None):
      possible = [ 'microover', 'smallover', 'midover', 'largeover' ]
      if cap is None:
          cap = 'midover'
      if isinstance(cap, str) is False:
          cap = 'midover'
      if cap not in possible:
          cap = 'midover'
      return cap

    def get_target(self, target=None):
        possible = [ 50 , 40 , 30 ]
        if target is None:
            target = 50
        try:
            target = int(target)
        except ValueError:
            target = 50
        if target not in possible:
            target = 50
        return str(target)

    def get_sh_price(self, sh_price=None):
        possible = [ 1, 2, 3, 4, 5, 7, 10 ]
        if sh_price is None:
            sh_price = 5
        try:
            sh_price = int(sh_price)
        except ValueError:
            sh_price = 5
        if sh_price not in possible:
            sh_price = 5
        return str(sh_price)

    def get_symbol_data(self, end):
        response = requests.get(end, headers={'User-Agent': 'curl/7.61.1','Accept': '*/*'})
        soup = BeautifulSoup(response.text, "html.parser")
        data = soup.prettify()
        data = data.partition('<!-- TS')
        final = ''
        for x in data:
            if 'TE -->' in x:
              final = x.partition('TE -->')[0]
              break
        if len(final) == 0:
            return None
        lines = final.split("\n")
        non_empty_lines = [line for line in lines if line.strip() != ""]
        symbols = []
        for symbol in non_empty_lines:
            symbols.append(symbol.split('|')[0])
        return symbols
        
    def get_symbols(self, an_recom=None, cap=None, target=None, sh_price=None):
        symbols = []
        an_recom = self.get_an_recom(an_recom)
        cap = self.get_cap(cap)
        target = self.get_target(target)
        sh_price = self.get_sh_price(sh_price)
        r = 1
        end = "https://finviz.com/screener.ashx?v=111&f=an_recom_{an_recom},cap_{cap},geo_usa,sh_price_o{sh_price},targetprice_a{target}&r={r}".format(an_recom=an_recom, cap=cap, target=target,sh_price=sh_price, r=r)
        symbol_data = self.get_symbol_data(end)
        if symbol_data is None:
            return None
        symbols.extend(symbol_data)
        hold = False
        while hold is False:
            r = r + 20
            end = "https://finviz.com/screener.ashx?v=111&f=an_recom_{an_recom},cap_{cap},geo_usa,sh_price_o{sh_price},targetprice_a{target}&r={r}".format(an_recom=an_recom, cap=cap, target=target,sh_price=sh_price, r=r)
            symbol_data = self.get_symbol_data(end)
            if symbol_data is None:
                hold = True
            elif len(symbol_data) == 1:
                symbols.extend(symbol_data)
                hold = True
            else:
                symbols.extend(symbol_data)
        return sorted(set(symbols))

    def full(self):
        r = 1
        symbols = self.get_symbols(r)
        foo = False
        while foo == False:
            r = r + 20
            more_symbols = self.get_symbols(r)
            if len(more_symbols) == 1:
                symbols.extend(more_symbols)
                foo = True
            else:
                symbols.extend(more_symbols)
        return sorted(set(symbols))
