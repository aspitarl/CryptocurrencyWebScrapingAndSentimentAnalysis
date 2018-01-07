# grow_log: what it means to csv
import os
import datetime as dt
import pandas as pd

from web_scraper import scrape_subreddits, scrape_forums
from constants import subreddits_return

def utc_to_local(utc_dt):
    print(type(utc_dt))
    # UTC timestamp to local time
    return utc_dt.replace(tzinfo=dt.timezone.utc).astimezone(tz=None)

def update_csv(rawtext_csvfile = None, subreddits = None):

    if rawtext_csvfile == None:
        folder = os.path.dirname(os.path.abspath("__file__"))
        rawtext_csvfile = folder + "\\rawtext.csv"
    if subreddits == None:
        subreddits = subreddits_return()

    # KYLE DEBUG
    forum_urls = ["https://bitcointalk.org/index.php?board=5.0", "https://bitcointalk.org/index.php?board=7.0",
                  "https://bitcointalk.org/index.php?board=8.0"]
    allowed_domains = ["bitcointalk.org",]
    dates_forums, texts_forums= scrape_forums(forum_urls, allowed_domains, max_pages=20)

    file_exists = os.path.isfile(rawtext_csvfile)
    # KYLE DEBUG
    
    if(file_exists):
        rawtext_read = pd.read_csv(rawtext_csvfile, encoding = "ISO-8859-1")
        dates_rawtext_read = rawtext_read['dates']
        timestampcutoff = float(dates_rawtext_read.iloc[-1])
    else:
        datecutoff = dt.datetime(2017,12,25,0,0,0)
        timestampcutoff = datecutoff.timestamp()
        
    print("Scraping from " + str(utc_to_local(dt.datetime.fromtimestamp(timestampcutoff)))) 
    
    dates, texts = scrape_subreddits(subreddits, 20, timestampcutoff)
        
    raw_text = pd.DataFrame({'dates' : dates, 'texts' : texts})
    
    if(file_exists):
        raw_text.to_csv(rawtext_csvfile, mode = 'a+', header = False)
    else:
        raw_text.to_csv(rawtext_csvfile, mode = 'a+', header = True)

    print("Added " + str(len(dates)) + " new comments")
    



def read_from_csv(window = None, endtime = None, rawtext_csvfile = None):
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
    

