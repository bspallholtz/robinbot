#!/usr/bin/python3
import robin_stocks2 as robin_stocks
import configparser
import os
from barchart import Barchart
from new_finviz import FinViz
from work_sql import Track_Buys

b = Barchart()

config = configparser.ConfigParser()

#symbols = Get_symbols().get_symbols()

fv_symbols = FinViz().full

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

def divide_chunks(l, n):
    for i in range(0, len(l), n):
        yield l[i:i + n]

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

def get_rh_rating(symbol, analyst):
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
    if buy < analyst:
        return None
    hold = data['summary']['num_hold_ratings']
    sell = data['summary']['num_sell_ratings']
    total = buy + hold + sell
    per = buy / total * 100
    if per > 90:
        return True

def get_cp(symbol):
    data = robin_stocks.stocks.get_quotes(symbol)[0]['ask_price']
    return data
    
username, password = get_creds()
robin_stocks.login(username, password)
buys = []
bought_symbols = Track_Buys().get_symbols()

d = FinViz().full()
for symbol in d:
    if get_rh_rating(symbol, 10) is True and b.buy(symbol) is True:
        buys.append(symbol)

for symbol in buys:
    cp = get_cp(symbol)
    Track_Buys().buy(symbol, cp, True)

for symbol in bought_symbols:
    if symbol not in buys:
        cp = get_cp(symbol)
        Track_buys().update_price(symbol, False, cp)

exit()


def main(ar, tp, analyst ):
  print("Getting symbols with %s, target price %s percent above of current price, and at least %i analysts on RH with 90 percent buy rating" % (  ar, tp, analyst ))
  foo = fv_symbols(ar, tp)
  for symbol in foo:
      if get_rh_rating(symbol, analyst) is True:
          print("RH say %s is a BUY" % symbol)

ars = [ 'strongbuy', 'buyorbetter' ]
tps = [ 50, 40, 30 ]
analysts = [ 15 , 10 , 5 ]
for tp in tps:
    for ar in ars:
        for analyst in analysts:
          main(ar, tp, analyst)
