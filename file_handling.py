# grow_log: what it means to csv
import os
import datetime as dt
import pandas as pd

from web_scraper import scrape_subreddits, scrape_twitter
from web_scraper import utc_to_local
import constants



def update_csv( subreddits = None):
    # grow a log

    if subreddits == None:
        subreddits = constants.subreddits
        
    folder = os.path.dirname(os.path.abspath("__file__")) + "\\Raw_Data"
    rawtext_csvfile_reddit = folder + "\\rawtext_reddit.csv"
    rawtext_csvfile_twitter = folder + "\\rawtext_twitter.csv"
    
        
        
    """
    # KYLE DEBUG
    forum_urls = ["https://bitcointalk.org/index.php?board=5.0",
                  "https://bitcointalk.org/index.php?board=7.0",
                  "https://bitcointalk.org/index.php?board=8.0"]
    allowed_domains = ["bitcointalk.org",]
    dates_forums, texts_forums= scrape_forums(forum_urls, allowed_domains, max_pages=20)
    # KYLE DEBUG
    """
    
    
    timestampcutoff_twitter,file_exists = determine_timestampcutoff(rawtext_csvfile_twitter)

    print("Scraping twitter from " + str(utc_to_local(dt.datetime.fromtimestamp(timestampcutoff_twitter)))) 
    
    dates_twitter, texts_twitter = scrape_twitter(timestampcutoff_twitter)
    raw_text_twitter = pd.DataFrame({'dates' : dates_twitter, 'texts' : texts_twitter})

    if(len(dates_twitter)):
        if(file_exists):
            raw_text_twitter.to_csv(rawtext_csvfile_twitter, mode = 'a+', header = False)
        else:
            raw_text_twitter.to_csv(rawtext_csvfile_twitter, mode = 'a+', header = True)

    print("Added " + str(len(dates_twitter)) + " new comments")

    
    
    timestampcutoff_reddit,file_exists = determine_timestampcutoff(rawtext_csvfile_reddit)
    
    print("Scraping reddit from " + str(utc_to_local(dt.datetime.fromtimestamp(timestampcutoff_reddit)))) 

    dates_reddit, texts_reddit = scrape_subreddits(subreddits, 20, timestampcutoff_reddit)
    
    raw_text_reddit = pd.DataFrame({'dates' : dates_reddit, 'texts' : texts_reddit})

    if(len(dates_reddit)):
        if(file_exists):
            raw_text_reddit.to_csv(rawtext_csvfile_reddit, mode = 'a+', header = False)
        else:
            raw_text_reddit.to_csv(rawtext_csvfile_reddit, mode = 'a+', header = True)


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
