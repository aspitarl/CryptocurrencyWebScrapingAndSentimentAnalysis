import praw
import scrapy
import pickle
import os
import sys
import tweepy

from API_settings import twitter_key, twitter_secret,twitter_access_token, twitter_access_token_secret 

from datetime import datetime, date, time, timezone
from time import mktime
from bs4 import BeautifulSoup
from scrapy.crawler import CrawlerProcess
from scrapy.spiders import Rule
from scrapy.exceptions import CloseSpider
from scrapy.linkextractors import LinkExtractor
from API_settings import client_id, client_secret, user_agent

date_word_list = [
    'January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November',
    'December', 'Today'
]


class ForumSpider(scrapy.Spider):
    """
    Scrapy object to scrape bitcointalk and other forums, couldn't get it working correctly. 
    """
    name = "forums"
    auto_throttle_enabled = True
    download_delay = 1.5
    rules = (Rule(LinkExtractor(), callback="parse", follow=True),
             )

    def start_requests(self):
        self.pages_crawled = 0
        for url in self.start_urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        for link in LinkExtractor(allow_domains=self.allow_domains).extract_links(response):
            yield scrapy.Request(url=link.url, callback=self.read_posts_bitcointalk)

    def read_posts_bitcointalk(self, response):
        url_post_string = ['topic', ]
        if any(substring in response.url for substring in url_post_string):
            self.pages_crawled += 1
            self.check_max_pages()

            soup = BeautifulSoup(response.body, "html.parser")
            texts_raw = soup.find_all('div', class_="post")
            dates_raw = soup.find_all('div', class_="smalltext")

            dates = []
            for date in dates_raw:
                date = date.get_text()
                if any(substring in date for substring in date_word_list) and len(date) < 30:
                    date = convert_date_to_unix_time(date)
                    dates.append(date)

            texts = []
            for text in texts_raw:
                text = text.get_text().encode('utf-8')
                if not text.isdigit():
                    texts.append(text)

            filename_date = "temp_date_output.txt"
            filename_text = "temp_text_output.txt"

            try:
                os.remove(filename_date)
            except OSError:
                pass

            try:
                os.remove(filename_text)
            except OSError:
                pass

            with open(filename_date, "a") as f1:
                pickle.dump(dates, f1)

            with open(filename_text, "a") as f2:
                pickle.dump(texts, f2)

        url_board_string = ["board=5", "board=7", "board=8"]
        if any(substring in response.url for substring in url_board_string):
            self.parse(response)

    def check_max_pages(self):
        if self.pages_crawled > self.max_pages:
            raise CloseSpider(reason='Page number exceeded')

def utc_to_local(utc_dt):
    #sets the timezone of a timestamp object to local time
    return utc_dt.replace(tzinfo=timezone.utc).astimezone(tz=None)


def convert_date_to_unix_time(date_local):
    if 'Today at ' in date_local:
        date_local = date_local.replace('Today at ', '')
        midnight = float(mktime(datetime.combine(date.today(), time.min).timetuple()))
        date_local = midnight + mktime(datetime.strptime(date_local, "%I:%M:%S %p").timetuple())
    else:
        date_local = mktime(datetime.strptime(date_local, "%B %d, %Y, %I:%M:%S %p").timetuple())

    return date_local

def convert_unixarray_timesamparray(intarray_unix):
    datetimearray=[]
    for unix in intarray_unix:
        datetimearray.append(datetime.fromtimestamp(unix))
        
    return datetimearray


def scrape_forums(url, allowed_domain, max_pages):
    sys.setrecursionlimit(10000)
    process = CrawlerProcess({
        #'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
    })

    spider = ForumSpider()

    process.crawl(spider, start_urls=url, allow_domains=allowed_domain, max_pages=max_pages)
    process.start()
    process.stop()

    with open("temp_date_output.txt", "r") as f1:
        dates = pickle.load(f1)

    with open("temp_text_output.txt", "r") as f2:
        texts = pickle.load(f2)

    return dates, texts


def scrape_subreddit(subreddit, submission_limit):
    dates = []
    texts = []

    reddit = praw.Reddit(client_id=client_id,
                         client_secret=client_secret,
                         user_agent=user_agent)

    for submission in reddit.subreddit(subreddit).hot(limit=submission_limit):
        dates.append(submission.created_utc)
        texts.append(submission.selftext)

        for comment in submission.comments[:]:
            if hasattr(comment, 'created'):
                dates.append(comment.created_utc)
                texts.append(comment.body)
            else:
                pass
    
    return dates, texts


def scrape_subreddits(subreddits, submission_limit, timestampcutoff):
    dates_local = []
    texts_local = []
    for subreddit in subreddits:
        print("Scraping " + str(subreddit) + "...")
        dates_temp, texts_temp = scrape_subreddit(subreddit, submission_limit)

        dates_local += dates_temp
        texts_local += texts_temp
        
    zipped = sorted(zip(dates_local,texts_local))
    
    dates_local_temp= [x for x , y in zipped]
    texts_local_temp= [x for y , x in zipped]
    
    dates_local = []
    texts_local = []
    
    i=0
    for timestamp in dates_local_temp:
        if timestamp > timestampcutoff:
            dates_local.append(dates_local_temp[i])
            texts_local.append(texts_local_temp[i])
        i=i+1

    return dates_local, texts_local

def scrape_twitter(timestampcutoff):
    """
    Reads data off of a twitter account, note you are limited to 15 requests at atime
    it currrently reads page by page (20 tweets) until it reaches timestamp cutoff
    """
    dates_twitter = []
    texts_twitter = []
    
    auth = tweepy.OAuthHandler(twitter_key, twitter_secret)
    auth.set_access_token(twitter_access_token, twitter_access_token_secret)
    api = tweepy.API(auth)
    
    reached_timestamp=0
    page_number = 1
    while(reached_timestamp==0):
        print("reading page number " + str(page_number))
        try:
            public_tweets = api.home_timeline(page=page_number)
            for tweet in public_tweets:
                localtime = utc_to_local(tweet.created_at)
                localtime = localtime.timestamp()
                if(localtime > timestampcutoff ) :   
                    dates_twitter.append(localtime)
                    texts_twitter.append(tweet.text)
                else:
                    reached_timestamp=1
                    break
        except tweepy.error.RateLimitError:
            print("rate limit error")
            reached_timestamp == 2
            break
        page_number = page_number+1
    
    dates_twitter = list(reversed(dates_twitter))
    texts_twitter = list(reversed(texts_twitter))
    
    return dates_twitter, texts_twitter
