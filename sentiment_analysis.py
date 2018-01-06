import numpy as np
import math
from nltk.sentiment.vader import SentimentIntensityAnalyzer as SIA
import pandas as pd



def analyse_text(text, keywords):
    sia = SIA()

    sentiment_out = 0
    no_keyword_counter = 0
    for keyword in keywords:
        if keyword in text:
            sentiment = sia.polarity_scores(text)

            sentiment = sentiment['compound']
            sentiment_out += sentiment
        else:
            no_keyword_counter += 1

    if no_keyword_counter == len(keywords):
        sentiment_out = np.nan

    return sentiment_out


def analyse_sentiments(dates_local, texts_local, keywords):
    sentiments_local = []
    dates_new = []
    texts_new = []
    sentiments_new = []

    for i in range(len(texts_local)):
        if isinstance(texts_local[i], str):
            result= analyse_text(texts_local[i], keywords)
            sentiments_local.append(result)
    
            if not math.isnan(sentiments_local[-1]):
                dates_new.append(dates_local[i])
                texts_new.append(texts_local[i])
                sentiments_new.append(sentiments_local[-1])

    return dates_new, texts_new, sentiments_new



def analyse_data(dates, texts, keywords = None):
    if keywords == None:
        keywords = {
                'BTC': {
                        'keywords' : ['bitcoin', 'bitcoins', 'xbt', 'btc', 'Bitcoin', 'Bitcoins', 'BTC', 'XBT']},
                'ETH': {
                        'keywords' : ['ethereum', 'Ethereum', 'eth', 'ETH', 'ether', 'Ether']},
                'LTC': {
                        'keywords' : ['litecoin', 'Litecoin', 'ltc', 'LTC']}
                }
    currencies = pd.DataFrame(keywords)
    currencies = currencies.T
    
        #analyse the recieved text
    num_currencies = currencies.shape[0]
    
    sentiments = [[0]]*num_currencies
    date_coinspecific = [[0]]*num_currencies
    texts_coinspecific = [[0]]*num_currencies
    

    i=0
    for ticker, keywords in currencies.itertuples():
        print("Analysing " + str(ticker))
        date_coinspecific[i], texts_coinspecific[i], sentiments[i] = analyse_sentiments(dates.as_matrix(), texts.as_matrix(), keywords)
        i=i+1
        
    currencies['dates'] = pd.Series(date_coinspecific, index=currencies.index)
    currencies['texts_nltk'] = pd.Series(texts_coinspecific, index=currencies.index)
    currencies['sentiments'] = pd.Series(sentiments, index=currencies.index)
    
    return currencies
    