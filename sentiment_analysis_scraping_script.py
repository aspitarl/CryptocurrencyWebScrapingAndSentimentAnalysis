from file_handling import update_csv, read_from_csv
from sentiment_analysis import analyse_data
from display import plot_data


def shape_data(data_sentiment, time_window):
              
    data_shape = data_sentiment   
    
    return data_shape


if __name__ == '__main__':
    
    ####UPDATE CSV FILES####


    #TODO: have a dates and text column for each website(combine in data analysis?)    

    #update_csv()
    
    #pulls out     
    dates, texts = read_from_csv(24*60*60)
    
    data_sentiment = analyse_data(dates, texts)

    data_shape = shape_data(data_sentiment)

    plot_data(data_shape)

