#!/usr/bin/env python

import sys
import os
from os import listdir
from os.path import isfile, join

projectdir = os.path.join('/home', 'ubuntu', 'project_pol-media-use')
modulesdir = os.path.join(projectdir, 'modules')
logdir = os.path.join(projectdir, "logs")

sys.path.insert(0, modulesdir)

import re
import pandas as pd
import json
import ast
import datetime
from mp_checker import mp_check


# Parameters
datadir = os.path.join('/home', 'ubuntu', 'data', 'dk-news')
olddir = os.path.join('/home', 'ubuntu', 'data', 'dk-news', 'old_data')
outdir = os.path.join('/home', 'ubuntu', 'data', 'dk-news', 'latest_data')
datapath = os.path.join(datadir, 'articles')
savename_csv = f"articles_combined_{datetime.datetime.now().date()}.zip"
savename_json = f"articles_combined_{datetime.datetime.now().date()}.json"
outpath_csv = os.path.join(outdir, savename_csv)
outpath_json = os.path.join(outdir, savename_json)


# Reading in old datafiles
old_files = [join(olddir,f) for f in listdir(olddir) if isfile(join(olddir, f))]
old_files = [datafile for datafile in old_files if datafile.endswith('.json')]


# Look for latest file
try:
    latest_file = max(old_files, key=os.path.getctime)
    latest_file_exists = True
except ValueError:
    latest_file_exists = False
    


# Read in latest file
if latest_file_exists:
    with open(latest_file, 'r', encoding = 'utf-8') as f:
        articles_existing = json.load(f)
   
    last_encounter_time = max([article.get('encounter_datetime') for article in articles_existing])
else:
    last_encounter_time = '0'


# Reading in datafiles
datafiles = [join(datapath,f) for f in listdir(datapath) if isfile(join(datapath, f))]
datafiles = [datafile for datafile in datafiles if datafile.endswith('.json')]


# Combine articles to one list
articles_combined = list()

for datafile in datafiles:
    with open(datafile, 'r', encoding = 'utf-8') as f:
        articles = json.load(f)
    
    articles_combined = articles_combined + articles
        

# Filter for existing articles
articles_combined = [article for article in articles_combined if article.get('encounter_datetime') > last_encounter_time]


# Combine with existing
if latest_file_exists:
    articles_all = articles_existing + articles_combined
else:
    articles_all = articles_combined


# Exclude source
for entry in articles_all:
    if 'article_source' in entry:
        entry.pop('article_source')


# Output json
with open(outpath_json, 'w', encoding = 'utf-8') as f:
    json.dump(articles_all, f)
    

# Output csv
articles_df = pd.DataFrame.from_records(articles_all)

articles_df.to_csv(outpath_csv, index = False, compression = "zip")