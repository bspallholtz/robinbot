#!/usr/bin/python3
# -*- coding: utf-8 -*-
import requests
import re
from bs4 import BeautifulSoup
from custom_log import Custom_Logger

logger = Custom_Logger().write_log

class FinViz:
    def get_data(self, symbol):
        #end = "https://finviz.com/quote.ashx?t=%s&ty=c&p=d&b=1" % symbol
        end = "https://finviz.com/quote.ashx?t=%s&ty=c&p=d&b=1" % symbol
        page = requests.get(end)
        soup = BeautifulSoup(page.text, "html.parser")
        foo = {}
        mydivs = soup.findAll(True, {'class': ['snapshot-td2-cp', 'snapshot-td2']})
        for index, line in enumerate(mydivs):
            line = str(line)
            if 'body' in line:
                line = line.split('=')[6]
                line = re.sub('[()\[\]]', '', line)
                line = line.replace(" ", "_")
                key = line
                spot = index + 1
                value = str(mydivs[spot])
                value = re.sub('(?:</span>)', '', value)
                value = re.sub('(?:<span style="color:)', '', value)
                value = re.sub('(?:>#008800;")', '', value)
                value = re.sub('(?:>#aa0000;")', '', value)
                value = re.sub('(?:<small>)', '', value)
                value = value.split('<b>')
                value = str(value[1])
                value = value.split('</b>')[0]
                foo[key] = value
        if 'Analysts\'_mean_target_price_offsetx' not in foo.keys() or 'Analysts\'_mean_recommendation_1' not in foo.keys():
            logger('DEBUG', "%s done, ar or tp not in finviz" % symbol)
            return { 'ar' : None, 'tp': None }
        #Finviz analyst recommendation
        ar = foo['Analysts\'_mean_recommendation_1']
        #Finviz analyst target price
        tp = foo['Analysts\'_mean_target_price_offsetx']
        #Make sure AR and TP are valid
        if ar == '-' or tp == '-':
            logger('DEBUG', "%s done, could not get ar or tp data" % symbol)
            return { 'ar' : None, 'tp': None }
        else:
            #Set them to floats, and multiply them so we do easy calculations
            ar = float(ar)
            tp = float(tp)
            return { 'ar' : ar, 'tp': tp }
