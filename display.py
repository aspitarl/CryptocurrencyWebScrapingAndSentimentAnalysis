# -*- coding: utf-8 -*-


from matplotlib import pyplot as plt

import numpy as np

from web_scraper import convert_unixarray_timesamparray


    ####PLOT DATA#####

    #TODO: read analysis csv in a specified 
    #TODO: read price data csv

    #TODO: make into a function takes in just a dataframe (figures out num currencies)
    #TODO: rolling average (bin?, deal with blank streches with previous value?)
    #TODO: also plot price data (right axis?)
def plot_data(data_sentiment, time_array):
    
    num_data_sentiment = data_sentiment.shape[0]  
    figsize = plt.figaspect(1/num_data_sentiment)
    fig, axs = plt.subplots(1,num_data_sentiment,figsize=figsize) 
    axs_right = axs
    #for i in range(len(axs_right)):
    #    axs_right[i] = axs[i].twinx()
        
    
    i=0    
    for ticker, keywords, dates, texts, sentiments, mean, num_mentions in data_sentiment.itertuples():
        datesarray = convert_unixarray_timesamparray(dates)
        timegrid = convert_unixarray_timesamparray(time_array)
        #dates_minmax = [convert_unixarray_timesamparray(np.min(dates)),convert_unixarray_timesamparray(np.max(dates))]
        axs[i].plot(datesarray, sentiments, "ro-")
        axs[i].plot(timegrid, mean, "bo-")
        axs_right[i] = axs[i].twinx()
        axs_right[i].plot(timegrid, num_mentions, "go-")
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