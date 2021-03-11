#!/usr/bin/python3
import sqlite3
from datetime import datetime
import os.path

db_file = 'buys.db'

class database():
    def __init__(self):
        if not os.path.isfile(db_file):
            f = open(db_file,"w+")
            f.close()
        connection = sqlite3.connect(db_file)
        cursor = connection.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS algo_record ( id INTEGER PRIMARY KEY, symbol TEXT, action TEXT, price INTERGER, action_date TEXT)")
        connection.commit()
        cursor.execute("CREATE TABLE IF NOT EXISTS closed_positions ( id INTEGER PRIMARY KEY, symbol TEXT, buy_price INTERGER, buy_date TEXT, sell_price INTERGER, sell_date TEXT, profit INTERGER)")
        connection.commit()

    def detect_state(self, symbol):
        connection = sqlite3.connect(db_file)
        cursor = connection.cursor()
        cursor.execute("SELECT action FROM algo_record ORDER BY action_date DESC LIMIT 1")
        state = cursor.fetchall()
        if len(state) == 0:
            state = 'closed'
            return state
        state = state[0][0]
        if state == 'BUY':
            state = 'open'
        if state == 'SELL':
            state = 'closed'
        return state

    def execute(self, symbol, action, price):
        connection = sqlite3.connect(db_file)
        cursor = connection.cursor()
        cursor.execute("INSERT INTO algo_record (symbol,action,price,action_date) VALUES (?,?,?, datetime('now'))", ( symbol, action, price))
        connection.commit()
        return True

    def get_symbols(self):
        connection = sqlite3.connect(db_file)
        cursor = connection.cursor()
        cursor.execute("SELECT DISTINCT symbol from algo_record")
        data = cursor.fetchall()
        return data[0]

    def get_transactions(self, symbol):
        connection = sqlite3.connect(db_file)
        cursor = connection.cursor()
        sql = "SELECT * FROM algo_record WHERE symbol = '%s'" % symbol
        cursor.execute(sql)
        data = cursor.fetchall()
        return data

    def write_profit(self, symbol, buy_price,buy_date,sell_price,sell_date,profit):
        connection = sqlite3.connect(db_file)
        cursor = connection.cursor()
        cursor.execute("INSERT INTO closed_positions (symbol,buy_price,buy_date,sell_price, sell_date, profit) VALUES (?,?,?,?,?,?)", ( symbol, buy_price,buy_date,sell_price, sell_date,profit))
        connection.commit()
    
    def clear_profits(self):
        connection = sqlite3.connect(db_file)
        cursor = connection.cursor()
        cursor.execute("delete from closed_positions")
        connection.commit()


