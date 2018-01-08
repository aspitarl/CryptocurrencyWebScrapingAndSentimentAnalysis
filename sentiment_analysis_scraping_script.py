from file_handling import update_csv, read_from_csv, grid_data
from sentiment_analysis import analyse_data
from display import plot_data
import datetime as dt
import numpy as np
import constants

#TODO: incorporate price data
#TODO: somehow integrate differnent websites into one dataframe
#TODO: get bitcointalk working

if __name__ == '__main__':

    #pull in new data into the csv file or create it
    #note: this takes a while as it goes through every subreddit. you can run 
    #the script without updating the csv files. 
    update_csv()
    
    #create time window and uniformly spaced time array
    now = dt.datetime.now()
    now = int(now.timestamp())
    Lookback_time = 12*60*60
    timestep = 1*60*60
    time_array = np.arange(now-Lookback_time,now,timestep)
    
    #pulls out reddit data from the time window  
    dates_reddit, texts_reddit = read_from_csv(constants.rawtext_csvfile_reddit,Lookback_time)
    
    #analyse sentiments for reddit
    data_sentiment_reddit = analyse_data(dates_reddit, texts_reddit)   
    data_sentiment_reddit = grid_data(data_sentiment_reddit,time_array)   
    
    #plot reddit analysis
    plot_data(data_sentiment_reddit,time_array)
    
    """
    """
    #pull twitter data from time window
    dates_twitter, texts_twitter = read_from_csv(constants.rawtext_csvfile_twitter,Lookback_time)
    
    #analyse sentiments for twitter
    data_sentiment_twitter = analyse_data(dates_twitter, texts_twitter)
    data_sentiment_twitter = grid_data(data_sentiment_twitter,time_array)  

    #plot twitter analysis
    plot_data(data_sentiment_twitter, time_array)
    

