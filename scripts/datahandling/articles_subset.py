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

## Stubbing function
def stubber(singleurl):
    if not singleurl.endswith("/"):
        singleurl = singleurl + "/"
    # split on /
    split_url = singleurl.split("/")
    # remove empty strings
    if split_url[-1]=="":
        split_url.pop(-1)
    # remove numbers
    if split_url[-1].isdigit():
        split_url.pop(-1)
    # remove other string formatting
    if split_url[-1]=="?st=1":
        split_url.pop(-1)
    # return stub
    url_stub = '/'.join(split_url[:-1])

    if 'jyllands-posten' in url_stub:
        url_stub = '/'.join(url_stub.split("/")[:-1])
    elif 'politiken.dk' in url_stub:
        url_stub = '/'.join(url_stub.split("/")[:-1])
    
    return(url_stub)


## Get list of stubbed urls
stubbed = []
for url in urls:
    stubbed.append(stubber(url))

stubbed_set = set(stubbed)

## Filtered stubs based on stubbed urls
filter_stubs = ['livsstil.tv2.dk', 
                   'vejr.tv2.dk', 
                   'underholdning.tv2.dk',
                   'dr.dk/sporten/seneste-sport',
                   'sport.tv2.dk',
                   'livsstil.tv2.dk/mad',
                   'sport.tv2.dk/amerikansk-fodbold',
                   'dr.dk/drtv/program',
                   'ekstrabladet.dk/sport/',
                   'underholdning.tv2.dk/kendte',
                   'politiken.dk/viden/Tech',
                   'sport.tv2.dk/ovrig-sport',
                   'underholdning.tv2.dk',
                   'jyllands-posten.dk/nyviden',
                   'livsstil.tv2.dk/bolig',
                   'politiken.dk/debat/klummer',
                   'ekstrabladet.dk/underholdning/kongelige/udenlandskekongelige',
                   'nyheder.tv2.dk/tech',
                   'politiken.dk/sport/cykling',
                   'jyllands-posten.dk/podcast/hvemvindervalget',
                   'livsstil.tv2.dk',
                   'vejr.tv2.dk',
                   'dr.dk/drtv/kanal',
                   'ekstrabladet.dk/underholdning/filmogtv',
                   'ekstrabladet.dk/sport/anden_sport',
                   'politiken.dk/kultur/boger/interview_boger',
                   'jyllands-posten.dk/sport/fodbold',
                   'dr.dk/sporten',
                   'politiken.dk/oekonomi/bolig',
                   'politiken.dk/kultur/boger',
                   'ekstrabladet.dk/underholdning',
                   'politiken.dk/rejser',
                   'ekstrabladet.dk/sport/fodbold/',
                   'politiken.dk/underholdning/politiken_quiz',
                   'jyllands-posten.dk/rejser',
                   'politiken.dk/oekonomi/privatoekonomi',
                   'jyllands-posten.dk/kultur/anmeldelser/litteratur',
                   'dr.dk/stories/1288510966',
                   'jyllands-posten.dk/international/europa',
                   'politiken.dk/udland',
                   'ekstrabladet.dk/sport',
                   'jyllands-posten.dk/jperhverv',
                   'jyllands-posten.dk/international',
                   'dr.dk/nyheder/webfeature',
                   'ekstrabladet.dk/plus',
                   'preprod.dr.dk/engagement/taet-paa',
                   'politiken.dk/sport',
                   'ekstrabladet.dk/underholdning/udlandkendte',
                   'politiken.dk/kultur/set_og_hoert',
                   'politiken.dk/kultur/medier',
                   'politiken.dk/debat/ledere',
                   'dr.dk/engagement/taet-paa',
                   'politiken.dk/debat/kroniken',
                   'politiken.dk/udland/int_europa',
                   'dr.dk/nyheder/detektor',
                   'politiken.dk/debat/debatindlaeg',
                   'politiken.dk/ibyen',
                   'politiken.dk/indland/politik/folketingsvalg_2022/folketingsvalg_2022_liveblog',
                   'dr.dk/nyheder/udland',
                   'ekstrabladet.dk/nyheder/erhverv',
                   'ekstrabladet.dk/forbrug/Teknologi',
                   'nyheder.tv2.dk/video',
                   'politiken.dk/debat',
                   'dr.dk/feature',
                   'ekstrabladet.dk/underholdning/dkkendte',
                   'dr.dk/nyheder/politik/politiske-analyser',
                   'nyheder.tv2.dk/udland',
                   'nyheder.tv2.dk/business',
                   'jyllands-posten.dk/sport',
                   'ekstrabladet.dk/forbrug/sundhed',
                   'politiken.dk/underholdning/bagsiden',
                   'politiken.dk/fotografier',
                   'dr.dk/nyheder/politik/resultater',
                   'ekstrabladet.dk/sport/fodbold/dansk_fodbold/superligaen/broendby',
                   'underholdning.tv2.dk/royale',
                   'politiken.dk/live',
                   'politiken.dk/forbrugogliv/sundhedogmotion',
                   'nyheder.tv2.dk/live',
                   'ekstrabladet.dk/nyheder/lederen',
                   'livsstil.tv2.dk/sundhed',
                   'dr.dk/sporten/vinter-ol',
                   'ekstrabladet.dk/underholdning/livsstil',
                   ]

def is_relevant(url):
    if any([stub in url for stub in filter_stubs]): # link irrelevant if from one of the stubs
        return False
    else: # relevant if none of the above is met
        return True 

art_df = art_df.loc[art_df['article_link'].apply(is_relevant), :] # use function above to filter articles based on URL
print(art_df.shape) # after removing irrelevant links


# Handle datetime
art_df['article_datetime'] = pd.to_datetime(art_df['article_datetime'], utc = True).dt.tz_localize(None)

## Sort articles from before collection start
art_df = art_df.loc[art_df['article_datetime'] > '2020-09-01', :]
print(art_df.shape) # after date filter


# Add filename
filename_regex = re.compile('(?:https://)?(?:www\.)?(?:\w+\.?)+\.dk', re.IGNORECASE)

art_df['filename'] = ''

newspapers = list(art_df['newspaper_name'].unique())

art_df.loc[art_df['newspaper_name'] == 'Berlingske', 'filename'] = art_df.loc[art_df['newspaper_name'] == 'Berlingske', 'article_link'].apply(lambda url: re.sub(filename_regex, 'Berlingske', url).replace('/', '_') + '.html')
art_df.loc[art_df['newspaper_name'] == 'DR', 'filename'] = art_df.loc[art_df['newspaper_name'] == 'DR', 'article_link'].apply(lambda url: re.sub(filename_regex, 'DR', url).replace('/', '_') + '.html')
art_df.loc[art_df['newspaper_name'] == 'EB', 'filename'] = art_df.loc[art_df['newspaper_name'] == 'EB', 'article_link'].apply(lambda url: re.sub(filename_regex, 'EB', url).replace('/', '_') + '.html')
art_df.loc[art_df['newspaper_name'] == 'JP', 'filename'] = art_df.loc[art_df['newspaper_name'] == 'JP', 'article_link'].apply(lambda url: re.sub(filename_regex, 'JP', url).replace('/', '_') + '.html')
art_df.loc[art_df['newspaper_name'] == 'Politiken', 'filename'] = art_df.loc[art_df['newspaper_name'] == 'Politiken', 'article_link'].apply(lambda url: re.sub(filename_regex, 'Politiken', url).replace('/', '_') + '.html')
art_df.loc[art_df['newspaper_name'] == 'TV2', 'filename'] = art_df.loc[art_df['newspaper_name'] == 'TV2', 'article_link'].apply(lambda url: re.sub(filename_regex, 'TV2', url).replace('/', '_') + '.html')


# Save
out_n = 'articles_subset_2023-02-14.json'
out_p = join(data_path, out_n)

art_df.to_json(out_p, orient='records')