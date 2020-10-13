import sys
sys.path.append('../modules')
import twitter_scrape_profiles as tsp
import sys
import time
import datetime
import logging

logger = logging.getLogger(__name__)

def main():
    twitter_profiles = ['JosephineFock', 'TorstenGejl', 'Kristianthdahl', 'MrMesserschmidt', 'LiseBech', 'SorenPape', 
                    'metteabildgaard', 'orlaosterby', 'PSkipperEL', 'MaiVilladsen', 'pederhvelplund', 'AlexVanopslagh', 
                    'olebirkolesen', 'oestergaard', 'IdaAuken', 'stinuslindgreen', 'PiaOlsen', 'signe_munk', 'JakobEllemann', 
                    'aahlers', 'kimvalentinDK', 'MogensJensenS', 'DanJoergensen', 'Paulin_Anne', 'Rstoklund', 
                    'Isabella Arendt', 'ammitzbollbille']

    tweet_columns = ['id', 'conversation_id', 'created_at', 'date', 'time', 'timezone', 'user_id', 'username', 'name', 
                         'place', 'tweet', 'urls', 'replies_count', 'retweets_count', 'likes_count', 'hashtags', 'link', 
                         'retweet', 'user_rt_id', 'user_rt', 'retweet_id', 'reply_to', 'retweet_date']

    datadir = "../data/tweets/"

    end_time = datetime.datetime(2020, 8, 1)

    dt_now = datetime.datetime.now()

    while dt_now < end_time:
        tsp.update_tweets_data(twitter_profiles, tweet_columns, datadir)
        time_out = 24 * 60 * 60
        time.sleep(time_out)
        dt_now = datetime.datetime.now()

if __name__ == '__main__':
    FORMAT = '%(asctime)-15s %(message)s'
    logging.basicConfig(filename='./scraper.log', filemode='w', level=logging.INFO, format = FORMAT)
    main()