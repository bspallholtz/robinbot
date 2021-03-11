#!/usr/bin/python3
import yfinance as yf
import json
import datetime


symbol = 'BLBD'
oldest_analyst = datetime.datetime.now() + datetime.timedelta(days=-90)
oldest_analyst = oldest_analyst.timestamp()
#['Firm', 'To Grade', 'From Grade', 'Action']
data = yf.Ticker(symbol)
try:
    data = data.recommendations
except IndexError as e:
    print(e)
    exit()
data = data.to_json(orient="split")
data = json.loads(data)
for index, date in enumerate(data['index']):
    date = int(str(date)[:-3])
    start = None
    if date > oldest_analyst:
        start = index
        break
grades = []
if start = None:
    exit()
for analyst in data['data'][start:]:
        firm = analyst[0]
        to_grade = analyst[1]
        if to_grade == 'Buy':
            grades.append(1)
        if to_grade == 'Neutral' or to_grade == 'Equal-Weight':
            grades.append(0)
        if to_grade == 'Overweight':
            grades.append(0.5)
        if to_grade == 'Market Perform':
            grades.append(1.5)
        if to_grade == 'Outperform':
            grades.append(1.75)
        print(sum(grades)/len(grades))
        from_grade = analyst[2]
        action = analyst[3]
        if action == 'init' or action == 'main':
            from_grade = None
        print("The firm %s went from %s to %s and took the action %s" % ( firm, from_grade, to_grade, action))
        avg = sum(grades)/len(grades)
        if len(grades) > 10 and avg > 1.5:
            print('True')
