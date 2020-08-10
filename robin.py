#!/usr/bin/python3
import configparser
import os
import json

import robin_stocks2 as robin_stocks
from get_symbols import Get_symbols



config = configparser.ConfigParser()
symbols = Get_symbols().get_symbols()


def prompt_creds():
  if os.path.isfile('/home/ec2-user/.saver.cfg'):
    os.remove('/home/ec2-user/.saver.cfg')
  username = input ("Enter RobinHood username: ")
  password = input ("Enter RobinHood password: ")
  config.add_section('ROBINHOOD')
  config['ROBINHOOD']['username'] = username
  config['ROBINHOOD']['password'] = password
  with open('/home/ec2-user/.saver.cfg', 'w') as configfile:
    config.write(configfile)

def get_creds():
  if os.path.isfile('/home/ec2-user/.saver.cfg') is False:
    prompt_creds()
  data = config.read('/home/ec2-user/.saver.cfg')
  if config.has_section('ROBINHOOD') is False:
    prompt_creds()
  if config.has_option('ROBINHOOD', 'username') is False:
    prompt_creds()
  if config.has_option('ROBINHOOD', 'password') is False:
    prompt_creds()
  username = config['ROBINHOOD']['username']
  password = config['ROBINHOOD']['password']
  return username, password


def get_rh_rating(symbol):
    data = robin_stocks.stocks.get_ratings(symbol, info=None)
    if isinstance(data, str) is True:
        data = data.rstrip('\n')
        if len(data) == 0:
            return None
    if data is None:
        return None
    if data['summary'] is None:
        return None
    buy = data['summary']['num_buy_ratings']
    if buy < 15:
        return None
    hold = data['summary']['num_hold_ratings']
    sell = data['summary']['num_sell_ratings']
    total = buy + hold + sell
    per = buy / total * 100
    if per > 90:
        return { 'buy': buy, 'per': per }

username, password = get_creds()
robin_stocks.login(username, password)
data = {'AMZN': {'buy': 43, 'per': 91.48936170212765}, 'ARCC': {'buy': 15, 'per': 93.75}, 'BABA': {'buy': 57, 'per': 100.0}, 'BILI': {'buy': 21, 'per': 91.30434782608695}, 'CHNG': {'buy': 18, 'per': 100.0}, 'CNC': {'buy': 19, 'per': 95.0}, 'EDU': {'buy': 31, 'per': 100.0}, 'EPD': {'buy': 23, 'per': 92.0}, 'EXAS': {'buy': 16, 'per': 100.0}, 'FANG': {'buy': 33, 'per': 91.66666666666666}, 'GOOG': {'buy': 39, 'per': 90.69767441860465}, 'GOOGL': {'buy': 40, 'per': 90.9090909090909}, 'GWPH': {'buy': 17, 'per': 100.0}, 'HDB': {'buy': 39, 'per': 95.1219512195122}, 'HUYA': {'buy': 16, 'per': 94.11764705882352}, 'IBN': {'buy': 47, 'per': 97.91666666666666}, 'ICE': {'buy': 19, 'per': 95.0}, 'J': {'buy': 15, 'per': 100.0}, 'KB': {'buy': 25, 'per': 100.0}, 'LHX': {'buy': 16, 'per': 94.11764705882352}, 'MMP': {'buy': 20, 'per': 90.9090909090909}, 'MOMO': {'buy': 25, 'per': 100.0}, 'PBA': {'buy': 19, 'per': 90.47619047619048}, 'PE': {'buy': 32, 'per': 91.42857142857143}, 'PSX': {'buy': 21, 'per': 100.0}, 'PTON': {'buy': 23, 'per': 92.0}, 'QURE': {'buy': 17, 'per': 94.44444444444444}, 'RNG': {'buy': 22, 'per': 91.66666666666666}, 'RPD': {'buy': 15, 'per': 93.75}, 'SKM': {'buy': 25, 'per': 100.0}, 'SNE': {'buy': 19, 'per': 90.47619047619048}, 'SRPT': {'buy': 23, 'per': 95.83333333333334}, 'TOT': {'buy': 24, 'per': 96.0}, 'VICI': {'buy': 15, 'per': 93.75}, 'VLO': {'buy': 19, 'per': 90.47619047619048}, 'YY': {'buy': 23, 'per': 92.0}}
print(json.dumps(sorted(data.items(), key = lambda x: x[1]['buy'])))
exit()
data = {}
for symbol in symbols:
    print(symbol)
    rh_rating = get_rh_rating(symbol)
    if rh_rating is None:
        continue
    data[symbol] = rh_rating
