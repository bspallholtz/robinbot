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
    con = sqlite3.connect('buys.db')
    cur = con.cursor()
    cur.execute('select * from buys order by symbol')
    rows = cur.fetchall()
    return render_template("display.html",rows = rows)

