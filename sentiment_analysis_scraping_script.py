from sentiment_analysis import analyse_data

from file_handling import update_csv, read_from_csv

from display import plot_data



from file_handling import update_csv


if __name__ == '__main__':
    
    ####UPDATE CSV FILES####
    

    #TODO: have a dates and text column for each website(combine in data analysis?)    

<<<<<<< HEAD
    #update_csv()
    
    dates, texts = read_from_csv(24*60*60)
    
    data_sentiment = analyse_data(dates, texts)

    plot_data(data_sentiment)
=======

>>>>>>> 86af4b669a2f91b1f938fba67544a7189f0c86e3
