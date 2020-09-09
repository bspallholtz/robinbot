#!/usr/bin/python3
import sqlite3
from datetime import datetime
import os.path


class Track_Buys():
    def __init__(self):
        if not os.path.isfile('buys.db'):
            f = open('buys.db',"w+")
            f.close()
        connection = sqlite3.connect('buys.db')
        cursor = connection.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS buys ( symbol TEXT UNIQUE, buy_price INTERGER, current_price INTERGER, bot_recommends BOOL, buy_date TEXT)")
        connection.commit()

    def buy(self,symbol, cp, bot_recommends):
        if self.check_for_symbol(symbol) is True:
            return self.update_price(symbol, cp, bot_recommends)
        today = datetime.now().isoformat()
        connection = sqlite3.connect('buys.db')
        cursor = connection.cursor()
        cursor.execute("INSERT INTO buys ( symbol, buy_price, current_price, bot_recommends, buy_date) VALUES ( ?, ?, ?, ?, ?)", ( symbol, cp, cp , bot_recommends, today))
        cursor.close()
        connection.commit()
        return True

    def update_price(self, symbol, cp, bot_recommends):
        today = datetime.now().isoformat()
        connection = sqlite3.connect('buys.db')
        cursor = connection.cursor()
        cursor.execute("UPDATE buys set current_price = '%f', bot_recommends = '%s' WHERE symbol = '%s'" % ( float(cp), bot_recommends, symbol))
        cursor.close()
        connection.commit()
        return True

    def check_for_symbol(self, symbol):
        connection = sqlite3.connect('buys.db')
        cursor = connection.cursor()
        cursor.execute("SELECT symbol FROM buys WHERE symbol = '%s'" % symbol)
        data = cursor.fetchall()
        if len(data) > 0:
            return True
        else:
            return False

    def get_symbols(self):
        connection = sqlite3.connect('buys.db')
        cursor = connection.cursor()
        cursor.execute("SELECT symbol FROM buys")
        data = cursor.fetchall()
        bought_symbols = []
        for symbol in data:
            bought_symbols.append(symbol[0])
        return bought_symbols

    def get_oldest_trade(self):
        connection = sqlite3.connect('buys.db')
        cursor = connection.cursor()
        cursor.execute("SELECT buy_date FROM buys ORDER BY buy_date ASC LIMIT 1")
        return cursor.fetchall()[0][0]
