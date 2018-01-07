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
def plot_data(currencies):
    
    
    
    num_currencies = currencies.shape[0]  
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