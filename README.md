# DailyHODLScraper

This project is a web scraper designed to scrape 
The Daily HODL crypto news website. It scrapes
for Bitcoin and Ethereum related news articles
and collects 4 pieces of information from each
article: Headline of Article, Date of Article, 
Author and the Link to full Article. It then 
connects to the Kylin Network API and adds the 
prices of the related cryptocurrency for fixed
timeframes between 1 week before writing
and 90 days after writing. 

This dataset can be used for training machine
learning algorithms to understand how the price
Of the underlying asset changes based on the 
headlines of the article and keywords presented.
An understanding of sentiment of the crypto 
markets can be gained from this data as well as 
how much that manifests in price action of the
asset.

For use:
-All files (excluding the csv files) should be
downloaded into the directory. 
-First run DailyHodlScraper.py
-Next run addCryptoPrices.py
-Data should be available in 2 newly created CSV 
files bitcoinPricesAdded.csv &
ethereumPricesAdded.csv
-A use of API.py can be used if it is desired to
have the data accessible by URL


The completed dataset 
(Updated March 30, 2022) is accessible in JSON
format from: travnado300.pythonanywhere.com
