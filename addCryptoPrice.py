import pandas as pd
from datetime import datetime
import time
import math
import requests
from pycoingecko import CoinGeckoAPI

cg = CoinGeckoAPI()

hour = 3600
day = 86400
week = 604800
month = 2592000

cryptos = ['bitcoin', 'ethereum']
kylinPairs = {'bitcoin':'btc_usd', 'ethereum': 'eth_usd'}

def datesForPrice(df):
    dates = df['Date'].unique()
    unixnow = math.floor(time.time())
    unixtimes = {}
    for date in dates:
        unixtimes[date] = (int(time.mktime((datetime.strptime(date, '%B %d, %Y')).timetuple())))
    start = unixtimes[min(unixtimes, key=unixtimes.get)] - week
    end =  unixtimes[max(unixtimes)] + 3 * month
    if unixnow < end:
        end = unixnow
    datesForSearch = [start, end, unixtimes]
    return datesForSearch

# For Current price
def kylinPriceRequest(currencyPair):
    r = requests.get('https://api.kylin-node.co.uk/prices?currency_pairs=' + currencyPair[0] + '_' + currencyPair[1])
    kylinPriceResponse = dict(r.json())
    return kylinPriceResponse["payload"][2]["price"]

''' FOR FUTURE USE
def kylinPriceRequest(currencyPair, start, end, timeperiod):
    r = requests.get('https://api.kylin-node.co.uk/prices/hist?period=' + timeperiod + '&after=' + start + '&before=' + end + '&currency_pair=' + currencyPair)
    kylinPriceResponse = dict(r.json())
    return kylinPriceResponse
'''
for crypto in cryptos:
    df = pd.read_csv(str(crypto) + '.csv')
    df.drop(df.columns[0], axis=1, inplace=True) # removes double row number
    df['Crypto'] = crypto
    dateData = datesForPrice(df)
    unixConversion = dateData[2]
    priceActionDates = ['7 Days Before', '3 Days Before', '1 Day Before', 'Day of Writing', 'Next Day', '3 Days After', '7 Days After', '14 Days After', '30 Days After', '60 Days After', '90 Days After']
    priceActionDatesDict ={'7 Days Before': -7, '3 Days Before':-3, '1 Day Before':-1, 'Day of Writing': 0, 'Next Day': 1, '3 Days After': 3, '7 Days After': 7, '14 Days After': 14, '30 Days After':30, '60 Days After':60, '90 Days After':90}
    for priceDay in priceActionDates:
        df[priceDay] = df['Date']
        df[priceDay] = df[priceDay].replace(unixConversion) + (priceActionDatesDict[priceDay] * day)
    filename = crypto + 'UnixTimeAdded.csv'
    df.to_csv(filename)
