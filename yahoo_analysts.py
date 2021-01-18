#!/usr/bin/python3
import yfinance as yf
import json
import datetime


class Yahoo_Analysts():
  def is_buy(self, symbol):
    oldest_analyst = datetime.datetime.now() + datetime.timedelta(days=-180)
    oldest_analyst = oldest_analyst.timestamp()
    #['Firm', 'To Grade', 'From Grade', 'Action']
    data = yf.Ticker(symbol)
    try:
      data = data.recommendations
    except IndexError:
      return False
    except AttributeError:
      return False
    except KeyError:
      return False
    except:
      return False
    try:
      data = data.to_json(orient="split")
    except AttributeError:
      return False
    data = json.loads(data)
    start = None
    for index, date in enumerate(data['index']):
      date = int(str(date)[:-3])
      if date > oldest_analyst:
        start = index
        break
    grades = []
    if start is None:
      return False
    for analyst in data['data'][start:]:
      firm = analyst[0]
      to_grade = analyst[1]
      grade = None
      if to_grade == 'Buy':
        grade = 1
      if to_grade == 'Neutral' or to_grade == 'Equal-Weight' or to_grade == 'Hold' or to_grade == 'In-Line':
        grade = 0
      if to_grade == 'Overweight':
        grade = 0.5
      if to_grade == 'Market Perform' or to_grade == 'Perform' or to_grade == 'Sector Perform' or to_grade == 'Peer Perform' or to_grade == 'Sector Weight':
        grade = 1.5
      if to_grade == 'Outperform' or to_grade == 'Market Outperform' or to_grade == 'Sector Outperform' or to_grade == 'Positive':
        grade = 1.75
      if to_grade == 'Strong Buy':
        grade = 2
      if to_grade == 'Underweight' or to_grade == 'Underperform':
        grade = -1
      if to_grade == 'Sell':
        grade = -2
      if grade is None:
          print("Failed to set a grade to_grade = %s analyst is %s" % (to_grade, firm))
          exit()
          return False
      grades.append(grade)
      from_grade = analyst[2]
      action = analyst[3]
      if action == 'init' or action == 'main':
        from_grade = None
        #print("The firm %s went from %s to %s and took the action %s" % ( firm, from_grade, to_grade, action))

    #print(sum(grades)/len(grades))
    avg = sum(grades)/len(grades)
    if len(grades) > 5 and avg >= 1:
      return True
    return False
