import pandas as pd
from datetime import datetime
import time
import math
import requests

hour = 3600
day = 86400
week = 604800
month = 2592000

cryptos = ['bitcoin', 'ethereum']
kylinPairs = {'bitcoin':'btc_usd', 'ethereum': 'eth_usd'}

def datesForPrice(df):
    dates = df['Date'].unique()
    unixtimes = {}
    for date in dates:
        unixtimes[date] = (int(time.mktime((datetime.strptime(date, '%B %d, %Y')).timetuple())))
    start = unixtimes[min(unixtimes, key=unixtimes.get)] - week
    end =  unixtimes[max(unixtimes, key=unixtimes.get)] + 6 * month
    datesForSearch = [start, end, unixtimes]
    return datesForSearch

# For Current price
def kylinPriceRequestCurrent(currencyPair):
    r = requests.get('https://api.kylin-node.co.uk/prices?currency_pairs=' + currencyPair)
    kylinPriceResponse = dict(r.json())
    return kylinPriceResponse["payload"][0]["price"]

def kylinPriceRequest(currencyPair, start, end, timeperiod, priceDict):
    r = requests.get('http://api.kylin-node.co.uk/prices/hist?period=' + str(timeperiod) + '&after=' + str(start) + '&before=' + str(end) + '&currency_pair=' + currencyPair)
    kylinPriceResponse = dict(r.json())['payload']
    for OHLC in kylinPriceResponse:
        for i in range(0, 24):
            timeOfData = OHLC['open_time'] + i * hour # extrapolates across whole day
            priceDict[int(timeOfData)] = OHLC['open_price']
    
    return priceDict

def unixDict(unixStart, unixEnd, currencyPair):
    unixnow = math.floor(time.time())
    priceDict = {}
    currentPrice = kylinPriceRequestCurrent(currencyPair)
    for unix in range(unixStart, unixEnd, hour):
        if unix > unixnow:
            priceDict[int(unix)] = 'Future Time, data not yet availible Unix Timestamp: ' + str(unix) + ' Price as of writing: ' + str(currentPrice)
        else:
            priceDict[int(unix)] = 'Data Unavailible from current API Unix Timestamp: ' + str(unix)
    return priceDict
    
for crypto in cryptos:
    df = pd.read_csv(str(crypto) + '.csv')
    df.drop(df.columns[0], axis=1, inplace=True) # removes double row number
    df['Crypto'] = crypto
    datesForSearch = datesForPrice(df)
    unixConversion = datesForSearch[2]
    priceDict = unixDict(datesForSearch[0], datesForSearch[1], kylinPairs[crypto])
    priceData = kylinPriceRequest(kylinPairs[crypto], datesForSearch[0], datesForSearch[1], hour, priceDict)
    priceActionDates = ['7 Days Before', '3 Days Before', '1 Day Before', 'Day of Writing', 'Next Day', '3 Days After', '7 Days After', '14 Days After', '30 Days After', '60 Days After', '90 Days After']
    priceActionDatesDict ={'7 Days Before': -7, '3 Days Before':-3, '1 Day Before':-1, 'Day of Writing': 0, 'Next Day': 1, '3 Days After': 3, '7 Days After': 7, '14 Days After': 14, '30 Days After':30, '60 Days After':60, '90 Days After':90}
    for priceDay in priceActionDates:
        df[priceDay] = df['Date']
        df[priceDay] = df[priceDay].replace(unixConversion) + (priceActionDatesDict[priceDay] * day)
        df[priceDay] = df[priceDay].astype(int)
        df[priceDay] = df[priceDay].replace(priceData)
    filename = crypto + 'PricesAdded.csv'
    df.to_csv(filename)
