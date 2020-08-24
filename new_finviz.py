#!/usr/bin/python3
# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup

class FinViz():
    def get_symbols(self, r):
        end = "https://finviz.com/screener.ashx?v=111&f=an_recom_buybetter,cap_smallover,geo_usa,sh_price_o5,targetprice_a40&o=marketcap&r=%s" % r
        response = requests.get(end, headers={'User-Agent': 'curl/7.61.1','Accept': '*/*'})
        soup = BeautifulSoup(response.text, "html.parser")
        data = soup.prettify()
        data = data.partition('<!-- TS')
        for x in data:
            if 'TE -->' in x:
                final = x.partition('TE -->')[0]
                break
        lines = final.split("\n")
        non_empty_lines = [line for line in lines if line.strip() != ""]
        symbols = []
        for symbol in non_empty_lines:
            symbols.append(symbol.split('|')[0])
        return symbols

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
        return symbols
