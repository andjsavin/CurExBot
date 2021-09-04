import requests
import time
import math
import database
import datetime
import csv
import pandas as pd
import plotly.express as px
import os

if not os.path.exists("images"):
    os.mkdir("images")

db = database.dataBase()
db.setup()
api_key = 'gwq2EEzanIOfW94YeBAb'
url_list = 'https://fxmarketapi.com/apilive'
url_convert = 'https://fxmarketapi.com/apiconvert'
url_chart = 'https://fxmarketapi.com/apitimeseries'
#get all available currencies
json_list = ','.join(requests.get('https://fxmarketapi.com/apicurrencies?api_key=gwq2EEzanIOfW94YeBAb').json()['currencies'].keys()).replace('USD', '')


#compare currencies with base currency
def currency_list(base='USD'):
    if (base not in json_list and base != 'USD'):
        return 'Wrong base currency'
    curtime = math.ceil(time.time())
    dbItems = db.get_items(base)
    # check if there is a fresh exchange rate in database
    if (not dbItems) or (dbItems and (curtime - int(dbItems[0][3])) >= 600):
        # check if exchange rate is old then delete it
        if dbItems and (curtime - int(dbItems[0][3]) >= 600):
            db.delete_item(base)
        currencies = base + json_list
        currencies = currencies.replace(',',',' + base)
        response = requests.get(url_list + '?api_key=' + api_key + '&currency=' + currencies)
        #formatting bot response
        tuples = [[x.replace(base, ''), '{:.2f}'.format(y)] for x, y in response.json()['price'].items()]
        #addint values to database
        for x in tuples:
            db.add_item(base, x[0], x[1], str(response.json()['timestamp']))
        #more formatting
        tuples = [': '.join(x) for x in tuples]
        return base + ' to:\n' + '\n'.join(tuples)
    else:
        print('from database')
        return base + ' to:\n' + '\n'.join([x[1] + ': ' + x[2] for x in dbItems])

#exchange X amount of base to comp
def exchange_cur(base, comp, amount):
    if (base not in json_list and base != 'USD'):
        return 'Wrong base currency'
    if (comp not in json_list and comp != 'USD'):
        return 'Wrong compared currency'
    curtime = math.ceil(time.time())
    dbItems = db.get_exchange(base, comp)
    #check if there is a fresh exchange rate in database
    if (not dbItems) or (dbItems and (curtime - int(dbItems[0][3])) >= 600):
        #check if exchange rate is old then delete it
        if dbItems and (curtime - int(dbItems[0][3]) >= 600):
            db.delete_item_by_comp(base, comp)
        answer = requests.get(url_convert + '?api_key=' + api_key + '&from=' + base + '&to=' + comp + '&amount=' + str(amount)).json()
        response = str('{:.2f}'.format(answer['total']))
        #adding new item to database
        db.add_item(base, comp, str(answer['price']), curtime)
    else:
        response = str('{:.2f}'.format(float(db.get_exchange(base, comp)[0][2]) * amount))
    return str(amount) + ' of ' + base + ' in ' + comp + ' is ' + response

#draws graph with history of exchange rate
def history_chart(base, comp, days):
    if (base not in json_list and base != 'USD'):
        return 'Wrong base currency'
    if (comp not in json_list and comp != 'USD'):
        return 'Wrong compared currency'
    end_date = datetime.datetime.today().strftime('%Y-%m-%d')
    start_date = (datetime.datetime.today() - datetime.timedelta(days=days)).strftime('%Y-%m-%d')
    response = requests.get(url_chart + '?api_key=' + api_key + '&currency=' + base + comp + '&start_date=' + start_date + '&end_date=' + end_date + '&interval=hourly')
    x = response.json()['price'].keys()
    data = []
    for i in x:
        data.append([response.json()['price'][i][base+comp]['close'], i])
    with open(base+comp+'.csv', 'w', encoding='UTF8') as f:
        writer = csv.writer(f)
        writer.writerow(['rate', 'date'])
        writer.writerows(data)
    df = pd.read_csv(base+comp+'.csv')
    os.remove(base+comp+'.csv')
    fig = px.line(df, x='date', y='rate', title=base + ' to ' + comp + ' over last ' + str(days) + ' days')
    fig.write_image('images/'+base+comp+str(days)+'.png')
    return 'Showing graph'


