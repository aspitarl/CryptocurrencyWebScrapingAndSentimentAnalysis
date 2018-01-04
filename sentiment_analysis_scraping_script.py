from web_scraper import scrape_subreddits, scrape_forums, convert_unixarray_timesamparray
from sentiment_analysis import analyse_sentiments

import datetime as dt

import pandas as pd

from matplotlib import pyplot as plt

import numpy as np

import os


if __name__ == '__main__':
    
    ####UPDATE CSV FILES####
    
    folder = os.path.dirname(os.path.abspath(__file__))
    rawtext_csvfile = folder + "\\rawtext.csv"
    
    
    file_exists = os.path.isfile(rawtext_csvfile)
    
    if(file_exists):
        rawtext_read = pd.read_csv(rawtext_csvfile, encoding = "ISO-8859-1")
        dates_rawtext_read = rawtext_read['dates']
        timestampcutoff = float(dates_rawtext_read.iloc[-1])
    else:
        datecutoff = dt.datetime(2017,12,29,0,0,0)
        timestampcutoff = datecutoff.timestamp()
        
    data = {
            'BTC': {
                    'keywords' : ['bitcoin', 'bitcoins', 'xbt', 'btc', 'Bitcoin', 'Bitcoins', 'BTC', 'XBT']},
            'ETH': {
                    'keywords' : ['ethereum', 'Ethereum', 'eth', 'ETH', 'ether', 'Ether']},
            'LTC': {
                    'keywords' : ['litecoin', 'Litecoin', 'ltc', 'LTC']}
            }
    currencies = pd.DataFrame(data)
    currencies = currencies.T
    

    subreddits = ["cryptocurrency", "cryptomarkets", "bitcoin", "bitcoinmarkets"]


    #TODO: have a dates and text column for each website(combine in data analysis?)    

    """
    forum_urls = ["https://bitcointalk.org/index.php?board=5.0", "https://bitcointalk.org/index.php?board=7.0",
                  "https://bitcointalk.org/index.php?board=8.0"]
    allowed_domains = ["bitcointalk.org",]
    dates_forums, texts_forums= scrape_forums(forum_urls, allowed_domains, max_pages=20)
    """

    dates, texts = scrape_subreddits(subreddits, 2, timestampcutoff)
        
    raw_text = pd.DataFrame({'dates' : dates, 'texts' : texts})
    
    
    if(file_exists):
        raw_text.to_csv(rawtext_csvfile, mode = 'a+', header = False)
    else:
        raw_text.to_csv(rawtext_csvfile, mode = 'a+', header = True)
    
    #analyse the recieved text
    num_currencies = currencies.shape[0]
    
    sentiments = [[0]]*num_currencies
    date_coinspecific = [[0]]*num_currencies
    texts_coinspecific = [[0]]*num_currencies
    

    i=0
    for ticker, keywords in currencies.itertuples():
        date_coinspecific[i], texts_coinspecific[i], sentiments[i] = analyse_sentiments(dates, texts, keywords)
        i=i+1
        
    currencies['dates'] = pd.Series(date_coinspecific, index=currencies.index)
    currencies['texts_nltk'] = pd.Series(texts_coinspecific, index=currencies.index)
    currencies['sentiments'] = pd.Series(sentiments, index=currencies.index)
    
    #TODO: append to analysis csv file

    ####PLOT DATA#####

    #TODO: read analysis csv in a specified 
    #TODO: read price data csv

    #TODO: make into a function takes in just a dataframe (figures out num currencies)
    #TODO: rolling average (bin?, deal with blank streches with previous value?)
    #TODO: also plot price data (right axis?)
    figsize = plt.figaspect(1/num_currencies)
    fig, axs = plt.subplots(1,num_currencies,figsize=figsize)
    
    i=0    
    for ticker, keywords, dates, texts, sentiments in currencies.itertuples():
        datesarray = convert_unixarray_timesamparray(dates)
        #dates_minmax = [convert_unixarray_timesamparray(np.min(dates)),convert_unixarray_timesamparray(np.max(dates))]
        axs[i].plot(datesarray, sentiments, "ro-")
        axs[i].set_title(ticker)
        #axs[i].set_xticks([dates_minmax[0],dates_minmax[1]])
        i=i+1
    
    plt.tight_layout()
    fig.autofmt_xdate()
    plt.show()
    """
    for currency in currencies:
        ticker = currency[0]
        keywords = currency[1]
        #dates, texts, sentiments = analyse_sentiments(dates, texts, keywords)
        #plt.plot(dates, sentiments, "o")
        #plt.show()
        i=i+1
    """