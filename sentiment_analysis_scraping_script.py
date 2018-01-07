from file_handling import update_csv, read_from_csv
from sentiment_analysis import analyse_data
from display import plot_data
import os
import datetime as dt
import numpy as np
import constants
import pandas as pd

from web_scraper import utc_to_local


def shape_data(data_sentiments, time_array):
    
    sentiments_grid = pd.DataFrame(constants.keywords)
    sentiments_grid = sentiments_grid.T
    
    num_ticker = sentiments_grid.shape[0]
    
    j=0
    mean = [[0]]*num_ticker
    num_mentions = [[0]]*num_ticker
    for ticker, keywords, dates,texts_nltk, sentiments in data_sentiments.itertuples():
        
        time_window = time_array[1] - time_array[0]
        
        mean_coinspecific = np.zeros(len(time_array))
        num_mentions_coinspecific= np.zeros(len(time_array))
        
        i=0
        for time in time_array:
            starttime = time-time_window/2
            endtime = time+time_window/2
            diff_start = abs(dates - starttime)
            index_start = diff_start.argmin()
            diff_end = abs(dates - endtime)
            index_end = diff_end.argmin()
            sentiments_subset = np.asarray(sentiments[index_start:index_end])
            mean_coinspecific[i] = sentiments_subset.mean()
            num_mentions_coinspecific[i] =index_end - index_start
            i=i+1
        
        mean[j] = mean_coinspecific
        num_mentions[j] = num_mentions_coinspecific
        j = j + 1
        
    data_sentiments['mean'] = mean
    data_sentiments['num mentions'] = num_mentions
    
    return data_sentiments


if __name__ == '__main__':
    
    ####UPDATE CSV FILES####
    
    folder = os.path.dirname(os.path.abspath("__file__")) + "\\Raw_Data"
    rawtext_csvfile_reddit = folder + "\\rawtext_reddit.csv"
    rawtext_csvfile_twitter = folder + "\\rawtext_twitter.csv"

    #TODO: have a dates and text column for each website(combine in data analysis?)    

    update_csv()
    
    
    now = dt.datetime.now()
    #print(now)
    now = int(now.timestamp())
    #print(now)
    Lookback_time = 12*60*60
    
    timestep = 1*60*60
    time_array = np.arange(now-Lookback_time,now,timestep)
    
    #pulls out     
    dates_reddit, texts_reddit = read_from_csv(rawtext_csvfile_reddit,Lookback_time)
    data_sentiment_reddit = analyse_data(dates_reddit, texts_reddit)
    
    data_sentiment_reddit = shape_data(data_sentiment_reddit,time_array)  
    
    plot_data(data_sentiment_reddit,time_array)
    
    """
    """
    dates_twitter, texts_twitter = read_from_csv(rawtext_csvfile_twitter,Lookback_time)
    data_sentiment_twitter = analyse_data(dates_twitter, texts_twitter)
    
    data_sentiment_twitter = shape_data(data_sentiment_twitter,time_array)  

    plot_data(data_sentiment_twitter, time_array)
    

    #data_shape = shape_data(data_sentiment)


