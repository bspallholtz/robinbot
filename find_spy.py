#!/usr/bin/python3
import os
import configparser
import yfinance as yf
import statistics
import json
from work_sql import Track_Buys
import datetime
import robin_stocks2 as robin_stocks


config = configparser.ConfigParser()


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

username, password = get_creds()
robin_stocks.login(username, password)

def get_cp(symbol):
    data = robin_stocks.stocks.get_quotes(symbol)[0]['last_trade_price']
    return float(data)

oldest_buy = Track_Buys().get_oldest_trade()
print(oldest_buy)
exit()
oldest_buy = oldest_buy.split('T')[0]
oldest_buy = datetime.datetime.strptime(oldest_buy, '%Y-%m-%d')
oldest_minus_one = oldest_buy + datetime.timedelta(days=-5)
data = yf.download("SPY", start=oldest_minus_one, end=oldest_buy)
data = data.to_json(orient="split")
data = json.loads(data)
high = data['data'][-1][1]
high = float("%.2f" % round(high, 2))
current = get_cp('SPY')
print(high)
print(current)
#Track_Buys().buy(symbol, get_cp(symbol), True)
#Tack_Buys().buy('SPY', current, 
