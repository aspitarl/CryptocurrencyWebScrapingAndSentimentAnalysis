# grow_log: what it means to csv
import os
import datetime as dt
import pandas as pd

from web_scraper import scrape_subreddits, scrape_twitter
from web_scraper import utc_to_local
import constants

import numpy as np

def update_csv():
        
    #bitcoin talk forums, not currently working
    """
    forum_urls = ["https://bitcointalk.org/index.php?board=5.0",
                  "https://bitcointalk.org/index.php?board=7.0",
                  "https://bitcointalk.org/index.php?board=8.0"]
    allowed_domains = ["bitcointalk.org",]
    dates_forums, texts_forums= scrape_forums(forum_urls, allowed_domains, max_pages=20)
    """
    
    
    timestampcutoff_twitter,file_exists = determine_timestampcutoff(constants.rawtext_csvfile_twitter)

    print("Scraping twitter from " + str(utc_to_local(dt.datetime.fromtimestamp(timestampcutoff_twitter)))) 
    
    dates_twitter, texts_twitter = scrape_twitter(timestampcutoff_twitter)
    raw_text_twitter = pd.DataFrame({'dates' : dates_twitter, 'texts' : texts_twitter})

    if(len(dates_twitter)):
        if(file_exists):
            raw_text_twitter.to_csv(constants.rawtext_csvfile_twitter, mode = 'a+', header = False)
        else:
            raw_text_twitter.to_csv(constants.rawtext_csvfile_twitter, mode = 'a+', header = True)

    print("Added " + str(len(dates_twitter)) + " new comments")

    
    
    timestampcutoff_reddit,file_exists = determine_timestampcutoff(constants.rawtext_csvfile_reddit)
    
    print("Scraping reddit from " + str(utc_to_local(dt.datetime.fromtimestamp(timestampcutoff_reddit)))) 

    dates_reddit, texts_reddit = scrape_subreddits(constants.subreddits, 20, timestampcutoff_reddit)
    
    raw_text_reddit = pd.DataFrame({'dates' : dates_reddit, 'texts' : texts_reddit})

    if(len(dates_reddit)):
        if(file_exists):
            raw_text_reddit.to_csv(constants.rawtext_csvfile_reddit, mode = 'a+', header = False)
        else:
            raw_text_reddit.to_csv(constants.rawtext_csvfile_reddit, mode = 'a+', header = True)


    print("Added " + str(len(dates_reddit)) + " new comments")
    
    
def determine_timestampcutoff(rawtext_csvfile):
    file_exists = os.path.isfile(rawtext_csvfile)

    if(file_exists):
        rawtext_read = pd.read_csv(rawtext_csvfile, encoding = "ISO-8859-1")
        dates_rawtext_read = rawtext_read['dates']
        timestampcutoff = float(dates_rawtext_read.iloc[-1])
    else:
        datecutoff = constants.timestart
        timestampcutoff = datecutoff.timestamp()
        
    return timestampcutoff, file_exists
    
def read_from_csv(rawtext_csvfile, window = None, endtime = None):
    if rawtext_csvfile == None:
        folder = os.path.dirname(os.path.abspath("__file__"))
        rawtext_csvfile = folder + "\\rawtext.csv"

    rawtext_read = pd.read_csv(rawtext_csvfile, encoding = "ISO-8859-1")
    dates_rawtext_read = rawtext_read['dates']
    texts_rawtext_read = rawtext_read['texts']

    if endtime == None:
        endtime = dates_rawtext_read.iloc[-1]
    if window == None:
        window = 24*60*60
    starttime = endtime - window

    diff_start = abs(dates_rawtext_read - starttime)
    index_start = diff_start.idxmin()
    diff_end = abs(dates_rawtext_read - endtime)
    index_end = diff_end.idxmin()

    starttimestr = str(utc_to_local(dt.datetime.fromtimestamp(starttime)))
    endtimestr = str(utc_to_local(dt.datetime.fromtimestamp(endtime)))

    print("Reading file from " + starttimestr + " to " + endtimestr)
    print("contains " + str(index_end - index_start) + " comments")

    dates = dates_rawtext_read[index_start:index_end]
    texts = texts_rawtext_read[index_start:index_end]

    return dates, texts


def grid_data(data_sentiments, time_array):
    """
    Takes unevenly spaced comments and bins them into windows that are evenly spaced
    determined by time_array. Returns average sentiment and number of mentions 
    within that window
    """
    
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
