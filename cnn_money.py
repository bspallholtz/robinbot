#!/usr/bin/python3
import requests
from bs4 import BeautifulSoup

class Money():
    def get_data(self, symbol):
        end = "https://money.cnn.com/quote/forecast/forecast.html?symb=%s" % symbol
        r = requests.get(end, headers={'User-Agent': 'curl/7.61.1','Accept': '*/*'})
        if r.status_code != 200:
            return False
        data = r.text
        soup = BeautifulSoup(data, "lxml")
        try:
            data = soup.find(class_="wsod_twoCol clearfix").get_text()
        except:
            return False
        data = data.split(',')
        if 'There is no forecast data available.' in data[0]:
            return False
        num_anal = int(data[0].split()[1])
        median_price = data[0].split()[-1]
        if '+' not in data[1]:
            return False
        percent = float(data[1].split('%')[0].split('+')[-1])
        if num_anal > 10 and percent > 30:
            return True

