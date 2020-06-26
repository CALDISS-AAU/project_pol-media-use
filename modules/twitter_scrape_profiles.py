import pandas as pd
import twint
import nest_asyncio 
import datetime
import os
nest_asyncio.apply()

import logging

logger = logging.getLogger(__name__)

def scrape_user(profile, date, datadir, columns):
    filename = profile + '.csv'
    dt_now = datetime.datetime.now().strftime("%b %d %Y %H:%M")
    
    c = twint.Config()
    c.Username = profile
    c.Since = date
    c.Store_csv = True
    c.Hide_output = True
    c.Custom['tweet'] = columns
    c.Output = datadir + filename
    
    print("{time}: Running scrape for {user}".format(time = dt_now, user = profile))
    logger.info("{time}: Running scrape for {user}".format(time = dt_now, user = profile))
    twint.run.Search(c)

def newline_fix(tweet):
    new_tweet = tweet.replace('    n', ' ')
    return(new_tweet)

def import_tweets(profile, datadir):
    filename = datadir + profile + '.csv'
    
    tweets = pd.read_csv(filename)
    tweets['tweet'] = tweets['tweet'].map(newline_fix)
    
    return(tweets)

def combine_tweets(twitter_profiles, tweet_columns, datadir):
    tweets_all = pd.DataFrame(columns = tweet_columns)
    
    for profile in twitter_profiles:
        try:
            tweets = import_tweets(profile, datadir)
            tweets_all = tweets_all.append(tweets, ignore_index = True)
        except IOError:
            logger.warning("No data file for {profile}".format(profile = profile))
            
        
    return(tweets_all)

def update_tweets_data(twitter_profiles, tweet_columns, datadir):
    dt_now = datetime.datetime.now().strftime("%b %d %Y %H:%M")
    logger.info("{dt_now}: Updating twitter data...".format(dt_now = dt_now))
    
    if not os.path.isdir(datadir):
        os.mkdir(datadir)
    
    run_date_default = "2020-01-01 08:00:00"
    
    try:
        with open(datadir + 'last_run_date.txt', 'r') as f:
            run_date = f.readline()
            f.close()
    except IOError:
        logger.warning("No existing log for last run time. Using default ({run_date})".format(run_date = run_date_default))
        run_date = run_date_default
        
    date_today = str(datetime.date.today())
    
    logger.info("Scraping profiles...")
    if date_today != run_date:
        for profile in twitter_profiles:
            scrape_user(profile, run_date, datadir, tweet_columns)
    
        logger.info("Combining data...")
        tweets_all_df = combine_tweets(twitter_profiles, tweet_columns, datadir)
    
        logger.info("Exporting data...")
        filename = "pol_tweets.csv"
    
        try:
            tweets_cache = pd.read_csv(datadir + filename)
            tweets_all_df = tweets_cache.append(tweets_all_df, ignore_index = True)
            tweets_all_df.drop_duplicates(inplace = True)
            tweets_all_df.to_csv(datadir + filename, index = False)
        except IOError:
            logger.warning("No cache file for tweets found. Creating new data file...")
            tweets_all_df.drop_duplicates(inplace = True)
            tweets_all_df.to_csv(datadir + filename, index = False)
        
        logger.info("Removing temporary data files...")
        for profile in twitter_profiles:
            try:
                os.remove(datadir + profile + ".csv")
            except IOError:
                continue
            
        
        with open(datadir + 'last_run_date.txt', 'w') as f:
            f.write(date_today)
    else:
        logger.info("No new data since last run.")
    logger.info("Update complete!")