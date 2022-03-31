import requests
from autoscraper import AutoScraper
import pandas as pd
from datetime import datetime
import time
import math
scraper = AutoScraper()

cryptos = ['bitcoin', 'ethereum']
URLs = {'bitcoin': 'https://dailyhodl.com/bitcoin-news/', 'ethereum': 'https://dailyhodl.com/ethereum/'}
pairs = {'bitcoin': 'btc_usd', 'ethereum': 'eth_usd'}

hour = 3600
day = 86400
week = 604800
month = 2592000

def produceURL(base, pageNumber):
    url = base + 'page/' + str(pageNumber) + '/'
    return url

def articleToDF(dataset):
    df = pd.DataFrame(dataset)
    df.columns = ['Title', 'Author', 'Date', 'Link']
    return(df) #.to_string())

def getHeadlines(baseURL):
    pageNumber = 1
    url = produceURL(baseURL, pageNumber)
    scraper.load('DailyHODLMaxPages')
    lastPage = int(scraper.get_result_similar(url)[0])
    scraper.load('HeadlineScraper')
    result = []
    for i in range (1, lastPage+1): #for i in range (1, 5):
        time.sleep(0.5)
        article = []
        pageNumber = i
        url = produceURL(baseURL, pageNumber)
        currentResults = scraper.get_result_similar(url, unique = False, keep_order=True, grouped = False)
        for articleData in currentResults:
            if 'http' in articleData:
                article.append(articleData)
                result.append(article)
                article = []
            else:
                article.append(articleData)
        print('Completed ' + str(i) + ' of ' + str(lastPage))
    result = articleToDF(result)
    return result

for crypto in cryptos:
    df = getHeadlines(URLs[crypto])
    filename = crypto + '.csv'
    df.to_csv(filename)