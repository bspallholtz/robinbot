#!/usr/bin/python3
import requests
import json
import configparser
import os

from custom_log import Custom_Logger

log = Custom_Logger().write_log

config = configparser.ConfigParser()

class Setup():
    def is_market_open(self):
        log("INFO", "Testing if market is open")
        end = 'https://financialmodelingprep.com/api/v3/is-the-market-open?apikey=07d01d0e9e3d5d7aef46d93a6a0c4529'
        data = requests.get(end)
        data = json.loads(data.text)
        return data['isTheStockMarketOpen']

    def prompt_creds(self):
        log('WARN', 'Prompting for creds for RH')
        if os.path.isfile('/home/ec2-user/.saver.cfg'):
            os.remove('/home/ec2-user/.saver.cfg')
            log('DEBUG', 'Removed /home/ec2-user/.saver.cfg')
        username = input ("Enter RobinHood username: ")
        log('DEBUG', 'Prompting user for username')
        password = input ("Enter RobinHood password: ")
        log('DEBUG', 'Prompting user for password')
        config.add_section('ROBINHOOD')
        config['ROBINHOOD']['username'] = username
        config['ROBINHOOD']['password'] = password
        with open('/home/ec2-user/.saver.cfg', 'w') as configfile:
            config.write(configfile)
        log('DEBUG', 'Wrote username and password to /home/ec2-user/.saver.cfg')
        return True

    def get_creds(self):
        log("INFO", "getting creds for RH")
        if os.path.isfile('/home/ec2-user/.saver.cfg') is False:
            self.prompt_creds()
        log("INFO", "getting creds for RH from local config file")
        config.read('/home/ec2-user/.saver.cfg')
        if config.has_section('ROBINHOOD') is False:
            self().prompt_creds()
        if config.has_option('ROBINHOOD', 'username') is False or config.has_option('ROBINHOOD', 'password') is False:
            self().prompt_creds()
        username = config['ROBINHOOD']['username']
        password = config['ROBINHOOD']['password']
        return username, password

