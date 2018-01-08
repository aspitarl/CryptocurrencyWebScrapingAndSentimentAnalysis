# -*- coding: utf-8 -*-


from matplotlib import pyplot as plt

import numpy as np

from web_scraper import convert_unixarray_timesamparray



    #TODO: also plot price data
    #TODO: figure out labeling
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
        axs[i].plot(datesarray, sentiments, "ro-",label = 'raw data')
        axs[i].plot(timegrid, mean, "bo-", label = 'average')
        axs_right[i] = axs[i].twinx()
        axs_right[i].plot(timegrid, num_mentions, "go-" , label = 'number_mentions')
        axs[i].set_title(ticker)
        #axs[i].set_xticks([dates_minmax[0],dates_minmax[1]])
        i=i+1
    
    #handles, labels = axs[0].get_legend_handles_labels()
    #axs[0].legend(handles, labels, loc='upper center', bbox_to_anchor=(0.5,-0.1))
    
    #fig.legend()
    
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