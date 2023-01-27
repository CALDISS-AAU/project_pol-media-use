#!/usr/bin/env python
# coding: utf-8

# Packages
import json
import os
from os.path import join
import re
import time
import pandas as pd
import random
import urllib
from urllib.parse import urlparse
from plotnine import *
from datetime import datetime

# Dirs
data_path = os.path.join('/work', 'polmeduse', 'data', 'dk_news')
articles_path = os.path.join(data_path, 'articles')

if not os.path.isdir(articles_path):
    os.mkdir(articles_path)

# Datafiles
rawdata_n = 'articles_combined_2022-12-08.json'
rawdata_p = os.path.join(data_path, rawdata_n)

# Load data
with open(rawdata_p, 'r', encoding = 'utf-8') as f:
    rawdata = json.load(f)

# Convert to pandas
art_df = pd.DataFrame.from_records(rawdata)
print(art_df.shape) # initial

# Remove duplicates
art_df = art_df.drop_duplicates(subset = ['article_link'])
print(art_df.shape) # after removing duplicates

# Filter irrelevant URLs
urls = list(art_df['article_link'])
urls_main = list(set([urlparse(url).netloc for url in urls])) # Main domains

def is_irrelevant(url):
    polit_stubs = ['dr.dk/nyheder/politik/', 'politiken.dk/indland/politik/', 'berlingske.dk/nyheder/politik', 
                   'berlingske.dk/politik/', 'nyheder.tv2.dk/politik/', 'ekstrabladet.dk/nyheder/politik/', 
                   'jyllands-posten.dk/politik/']
    irrelevant_mains = ['livsstil.tv2.dk', 'sport.tv2.dk', 'vejr.tv2.dk', 'underholdning.tv2.dk']

    if urlparse(url).netloc in irrelevant_mains: # link irrelevant is from irrelevant main domain
        return True
    elif not any([stub in url for stub in polit_stubs]): # link irrelevant if not from policy section
        return True
    else: # relevant if none of the above is met
        return False 

art_df = art_df.loc[~art_df['article_link'].apply(is_irrelevant), :] # use function above to filter articles based on URL
print(art_df.shape) # after removing irrelevant links

# Handle datetime
art_df['article_datetime'] = pd.to_datetime(art_df['article_datetime'], utc = True).dt.tz_localize(None)

## Sort articles from before collection start
art_df = art_df.loc[art_df['article_datetime'] > '2020-09-01', :]
print(art_df.shape) # after date filter

# Counts
count_df = art_df.groupby(['newspaper_name', art_df['article_datetime'].dt.year, art_df['article_datetime'].dt.month]).agg('size').to_frame(name = 'count').reset_index(names = ['newspaper', 'year', 'month'])
count_df['year-month'] = count_df['year'].astype('str') + count_df['month'].astype('str').str.pad(2, fillchar = '0')
count_df = count_df.sort_values('year-month')


## Counts visualization
count_plot = (ggplot(count_df, aes(x = 'year-month', y = 'count', group = 'newspaper', colour = 'newspaper')) + 
    geom_line() + 
    theme(axis_text_x = element_text(angle = 90))
)

count_plot.save('count_plot.png') # save plot