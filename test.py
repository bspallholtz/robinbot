#!/usr/bin/python3
import robin_stocks2 as robin_stocks
import os
import configparser

config = configparser.ConfigParser()

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
id = 'a5fc2769-bead-4e6a-bc25-deffe159d3c0'
buy_data = robin_stocks.orders.get_stock_order_info(id)
print(buy_data['state'])
