#!/usr/bin/env python

import pandas as pd
import json
import os
from os import listdir
from os.path import isfile, join
import multiprocessing as mp
import ast
import numpy as np
import datetime

# Parameters
poolsize = 8
#datadir = os.path.join('D:/', 'data', 'poltweets')
datadir = os.path.join('/home', 'ubuntu', 'data', 'poltweets', 'latest_data')
datafiles = [join(datadir,f) for f in listdir(datadir) if isfile(join(datadir, f))]
datafile = [datafile for datafile in datafiles if (datafile.startswith('poltweets_combined') & datafile.endswith('.gz'))][0]
outname = f'poltweets_flattened_{datetime.datetime.now().date()}.gz'

datapath = os.path.join(datadir, datafile)
savepath = os.path.join(datadir, outname)

import_cols = ['created_at', 'id', 'full_text', 'entities', 'user', 'retweeted_status', 'is_quote_status', 'retweet_count', 
            'favorite_count', 'favorited', 'retweeted']
user_infos = ['id', 'name', 'screen_name', 'location', 'description', 'url', 'followers_count', 'created_at', 'verified']
keep_cols = ['created_at', 'id', 'full_text', 'is_quote_status', 'retweet_count', 'favorite_count', 'favorited', 'retweeted',
            'is_retweet', 'hashtags', 'user_mentions', 'urls'] + ["user_" + user_info for user_info in user_infos]


def fix_dicts(string):
    if not isinstance(string, dict):
        string_as_dict = ast.literal_eval(string)
        return(string_as_dict)
    else:
        return(string)

def unnest_hashtags(hashtags):
    if isinstance(hashtags, list):
        hashtags_list = [hashtag.get('text') for hashtag in hashtags]
        return(hashtags_list)
    else:
        return

def process_df(df, keep_cols = 'all', user_infos = 'all'):
    df = df.dropna(subset = ['user'])
    df = df.reset_index()
    df['is_retweet'] = df['retweeted_status'].notna()
    df['entities'] = df['entities'].apply(fix_dicts)
    df['user'] = df['user'].apply(fix_dicts)
    df = pd.concat([df, pd.json_normalize(df['entities'], max_level = 1)], axis = 1)

    if user_infos == 'all':
        user_infos = list(df.loc[0, 'user'].keys())

    for user_info in user_infos:
        colname = "user_" + user_info
        try:
            df[colname] = df['user'].apply(lambda x: x.get(user_info))
        except TypeError:
            df[colname] = np.nan

    df['hashtags'] = df['hashtags'].apply(unnest_hashtags)  
    
    if keep_cols == 'all':
        return(df)
        
    else:
        df = df.loc[:, keep_cols]
        return(df)

def chunk_data(path, chunksize = 10000, cols = 'all'):
    if cols == 'all':
        import_cols = None
        
    for chunk in pd.read_csv(path, chunksize = chunksize, usecols = import_cols):
        yield chunk

def iter_process(datapath, poolsize = 4):
    processed_df = pd.DataFrame()
    pool = mp.Pool(poolsize)
    
    chunked_data = chunk_data(datapath)
    
    results = []
    for chunk in chunked_data:
        results.append(pool.apply_async(process_df, args = (chunk,)))
    
    dfs = [result.get() for result in results]    
    for df in dfs:
        processed_df = processed_df.append(df, ignore_index = True)
    
    return(processed_df)

def run_and_save(poolsize = 4):
    processed_df = iter_process(datapath, poolsize = poolsize)
    processed_df.to_csv(savepath, compression='gzip')

if __name__ == '__main__':
    run_and_save(poolsize)


    
