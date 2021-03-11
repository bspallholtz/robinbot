#!/usr/bin/python3.7
import json
import configparser
import os
from finviz import FinViz
from yahoo_analysts import Yahoo_Analysts
import robin_stocks
import smtplib, ssl
from work_sql import database
from custom_log import Custom_Logger
import configparser


config = configparser.ConfigParser()

port = 465  # For SSL
smtp_server = "smtp.gmail.com"
sender_email = "brian.stock.algo@gmail.com"
receiver_email = ["jss9631@gmail.com", "brian.spallholtz@gmail.com", "hfspro@yahoo.com"]
receiver_email = ["brian.spallholtz@gmail.com"]

possible_cap = [ 'microover', 'smallover', 'midover', 'largeover' ]
possible_tp = [ 50 , 40 , 30 ]
possible_sh_price = [ 1, 5, 10 ]
possible_an_recom = [ 'strongbuy', 'buybetter', 'buy' ]

log = Custom_Logger().write_log
database()
config = configparser.ConfigParser()

def prompt_creds():
  if os.path.isfile('/home/ec2-user/.saver.cfg'):
    os.remove('/home/ec2-user/.saver.cfg')
  username = input ("Enter RobinHood username: ")
  password = input ("Enter RobinHood password: ")
  username = input ("Enter Gmail username: ")
  password = input ("Enter Gmail password: ")
  config.add_section('ROBINHOOD')
  config.add_section('GMAIL')
  config['ROBINHOOD']['username'] = username
  config['ROBINHOOD']['password'] = password
  config['GMAIL']['username'] = username
  config['GMAIL']['password'] = password
  with open('/home/ec2-user/.saver.cfg', 'w') as configfile:
    config.write(configfile)

def get_creds():
  if os.path.isfile('/home/ec2-user/.saver.cfg') is False:
    prompt_creds()
  data = config.read('/home/ec2-user/.saver.cfg')
  if config.has_section('ROBINHOOD') is False:
    prompt_creds()
  if config.has_section('GMAIL') is False:
    prompt_creds()
  if config.has_option('ROBINHOOD', 'username') is False:
    prompt_creds()
  if config.has_option('ROBINHOOD', 'password') is False:
    prompt_creds()
  if config.has_option('GMAIL', 'username') is False:
    prompt_creds()
  if config.has_option('GMAIL', 'password') is False:
    prompt_creds()
  rh_username = config['ROBINHOOD']['username']
  rh_password = config['ROBINHOOD']['password']
  gmail_username = config['GMAIL']['username']
  gmail_password = config['GMAIL']['password']
  return rh_username,rh_password,gmail_username,gmail_password

def get_rh_rating(symbol):
    analysts = 10
    data = robin_stocks.stocks.get_ratings(symbol, info=None)
    if isinstance(data, str) is True:
        data = data.rstrip('\n')
        if len(data) == 0:
            return False
    if data is None:
        return False
    if data['summary'] is None:
        return False
    buy = data['summary']['num_buy_ratings']
    if buy < analysts:
        return False
    hold = data['summary']['num_hold_ratings']
    sell = data['summary']['num_sell_ratings']
    total = buy + hold + sell
    per = buy / total * 100
    if per > 90:
        return True
    return False

def get_cap(symbol):
    cap  = int(robin_stocks.stocks.get_fundamentals(symbol, info='market_cap')[0].split('.')[0])
    if cap > 20000000000:
        risk = 1
    if cap < 200000000000 and cap > 10000000000:
        risk = 2
    if cap < 10000000000 and cap > 2000000000:
        risk = 3
    if cap < 2000000000 and cap > 300000000:
        risk = 4
    if cap < 300000000 and cap > 50000000:
        risk = 5
    if cap < 50000000:
        risk = 6
    return risk

def get_price(symbol):
    price = float(robin_stocks.stocks.get_quotes(symbol)[0]['last_trade_price'])
    return price

def get_price_risk(price):
    if price < 1:
        risk = 5
    if price > 1 and price < 5:
        risk = 4
    if price > 5 and price < 10:
        risk = 3
    if price > 10 and price < 20:
        risk = 2
    if price > 20:
        risk = 1
    return risk

def get_data():
  symbols = {}
  tested = []
  buys = []
  for cap in possible_cap:
    symbols[cap] = {}
    for tp in possible_tp:
      symbols[cap][tp] = {}
      for sh_price in possible_sh_price:
        symbols[cap][tp][sh_price] = {}
        for an_recom in possible_an_recom:
          symbols[cap][tp][sh_price][an_recom] = {}
  for cap in symbols:
      for tp in symbols[cap]:
         for sh_price in symbols[cap][tp]:
             for an_recom in symbols[cap][tp][sh_price]:
                data = FinViz().get_symbols(cap=cap, target=tp, sh_price=sh_price, an_recom=an_recom)
                if data is None or len(data) == 0:
                    continue
                symbols[cap][tp][sh_price][an_recom] = []
                for symbol in sorted(set(data)):
                  if symbol not in tested:
                    tested.append(symbol)
                    if get_rh_rating(symbol) is True and Yahoo_Analysts().is_buy(symbol) is True:
                      buys.append(symbol)
                      symbols[cap][tp][sh_price][an_recom].append(symbol)
  return symbols


def execute(symbol):
    log('INFO', "Attempting a buy {symbol}".format(symbol=symbol))
    if database().detect_state(symbol) == 'closed':
        log('INFO', 'Position is closed, executing a buy')
        price = get_price(symbol)
        status = str(database().execute(symbol, 'BUY', price))
        log('INFO', status)
        return status
    else:
        log('INFO', 'Position is open, not buying')
        return True

def calculate_profit():
    database().clear_profits()
    symbols = database().get_symbols()
    for symbol in symbols:
        transactions = database().get_transactions(symbol)
        if database().detect_state(symbol) == 'open':
            transactions = transactions[:-1]
        if transactions[0][2] != 'BUY':
          log('ERROR', 'Something wrong with the transaction order, breaking')
          exit(1)
        for index, transaction in enumerate(transactions):
            if transaction[2] == 'SELL':
                continue
            buy_price = transaction[3] * -1
            buy_date = transaction[4]
            sell_price = transactions[index + 1][3]
            sell_date = transactions[index + 1][4]
            profit = buy_price + sell_price
            database().write_profit(symbol,buy_price,buy_date,sell_price,sell_date,profit)

def process():
    buys = []
    data = get_data()
    convert = { 'microover': '50 million', 'smallover' : '300 million', 'midover' : '2 billion', 'largeover' : '10 billion' }
    message = """\
Subject: Brian's algo stock pick's for today 


Below is the algorithm's output for today

Please review our disclaimer "future link to disclamer"

Email for quesitons: brian.stock.algo@gmail.com

Risk is based on market cap, stock price, volume, and volitility of the stock

The risk goes from 1 ( low ) to 5 ( high ) 

Star rating system key: 
   5   = Strong Buy, 50% upside
   4   = Strong Buy, 40% upside
   3   = Better Buy, 50% upside
   2   = Better Buy, 40% upside
   1.5 = Strong Buy, 30% upside
   1   = Better Buy, 30% upside

For a history of this algo's preformance look here - http://18.216.255.152:5000/profit

For information on method and sources look here - "future link describe method and sources"

Recommendation: Hold each symbol that is recommeneded for 12 months , set a stop loss price by percent depending on loss threshold.

"""
    for cap in data:
        for tp in data[cap]:
            for sh_price in data[cap][tp]:
                for an_recom in data[cap][tp][sh_price]:
                    if len(data[cap][tp][sh_price][an_recom]) == 0:
                            continue
                    for symbol in data[cap][tp][sh_price][an_recom]:
                        execute(symbol)
                        cap_risk = get_cap(symbol)
                        price_risk = get_price_risk(get_price(symbol))
                        risk = str(cap_risk / price_risk)
                        if tp == 50 and an_recom == 'strongbuy':
                            message = message + '5 Star: ' + symbol + ', Risk = ' + risk + '  \n\n'
                        elif tp == 40 and an_recom == 'strongbuy':
                            message = message + '4 Star: ' + symbol + ', Risk = ' + risk + '  \n\n'
                        elif tp == 50 and an_recom == 'buybetter':
                            message = message + '3 Star: ' + symbol + ', Risk = ' + risk + '  \n\n'
                        elif tp == 40 and an_recom == 'buybetter':
                            message = message + '2 Star: ' + symbol + ', Risk = ' + risk + '  \n\n'
                        elif tp == 30 and an_recom == 'buybetter':
                            message = message + '1 Star: ' + symbol + ', Risk = ' + risk + '  \n\n'
                        elif tp == 30 and an_recom == 'strongbuy':
                            message = message + '1.5 Star: ' + symbol + ', Risk = ' + risk + '  \n\n'
                        else:
                            print(symbol)
                            print(tp)
                            print(an_recom)
                            print(risk)
    calculate_profit()
    return message

rh_username, rh_password,gmail_username, gmail_password = get_creds()
robin_stocks.login(rh_username, rh_password)

context = ssl.create_default_context()
with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
    server.login(gmail_username, gmail_password)
    server.sendmail(sender_email, receiver_email, process())
