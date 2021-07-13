#!/usr/bin/env python

import sys
import os
from os import listdir
from os.path import isfile, join

projectdir = os.path.join(".")
modulesdir = os.path.join(projectdir, "modules")
datadir = os.path.join(projectdir, "data")
logdir = os.path.join(projectdir, "logs")

sys.path.insert(0, modulesdir)

import re
import pandas as pd
import json
import ast
from mp_checker import mp_check


# Parameters
maindir = os.path.join('D:/', 'data',  'dk_news')
datafolder = 'articles_20210421_with-text'
savename = "articles_combined_20210421.zip"


# Setting directories
datapath = os.path.join(maindir, datafolder)
outdir = os.path.join(maindir, savename)


# Reading in datafiles
datafiles = [join(datapath,f) for f in listdir(datapath) if isfile(join(datapath, f))]
datafiles = [datafile for datafile in datafiles if re.match(r'.*\.json', datafile)]


# Combine articles to dataframe
articles_df = pd.DataFrame()

for c, datafile in enumerate(datafiles, start = 1):
    articles_df = articles_df.append(pd.read_json(datafile), ignore_index = True)
    
    print("{:.2f}%".format(100.0*c/len(datafiles)), end = "\r")


# MP check
articles_df.loc[(articles_df['mp_matches'].isna()) & (articles_df['article_text'].notna()), 'mp_matches'] = articles_df.loc[(articles_df['mp_matches'].isna()) & (articles_df['article_text'].notna()), 'article_text'].apply(mp_check)

articles_df.loc[(articles_df['mp_match'].isna()) & (articles_df['article_text'].notna()), 'mp_match'] = articles_df.loc[(articles_df['mp_match'].isna()) & (articles_df['article_text'].notna()), 'mp_matches'].apply(lambda x: len(x) > 0)
    
articles_df.to_csv(outdir, index = False, compression = "zip")

