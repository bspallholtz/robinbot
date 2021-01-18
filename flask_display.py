#!/usr/bin/python3
#from flask import Flask,render_template
from flask import Flask, request, render_template

import time
import sqlite3
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/positions')
def display_table():
    con = sqlite3.connect('/home/ec2-user/robinbot/buys.db')
    cur = con.cursor()
    cur.execute('select * from buys order by symbol')
    rows = cur.fetchall()
    return render_template("display.html",rows = rows)

@app.route('/profit')
def display_foo():
    con = sqlite3.connect('/home/ec2-user/robinbot/buys.db')
    cur = con.cursor()
    cur.execute('select symbol, buy_price, current_price, bot_recommends, buy_date, round(((current_price - buy_price) / buy_price) * 100, 2 ) as profit from buys order by profit')
    rows = cur.fetchall()
    cur.execute('create view IF NOT EXISTS total_profit AS select "TOTAL" as symbol ,round(sum(buy_price), 2) as buy_price, round(sum(current_price), 2) as current_price, "TRUE" as bot_recommends, "NULL" as buy_date, round(((sum(current_price) - sum(buy_price))/sum(buy_price)) * 100, 2) as profit from buys WHERE symbol != "SPY"')
    cur.execute('select * from total_profit')
    rows.append(cur.fetchall()[0])
    return render_template("display_profit.html",rows = rows)

@app.route('/current_buys')
def display_buys():
    con = sqlite3.connect('/home/ec2-user/robinbot/buys.db')
    cur = con.cursor()
    cur.execute('select  symbol, buy_price, current_price, bot_recommends, buy_date, round(((current_price - buy_price) / buy_price) * 100, 0) as profit from buys where bot_recommends == "True" order by profit')
    rows = cur.fetchall()
    return render_template("display_profit.html",rows = rows)
