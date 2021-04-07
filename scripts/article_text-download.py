#!/usr/bin/env python
# coding: utf-8

# Packages
import os
import sys

projectdir = os.path.join("project_pol-media-use")
modulesdir = os.path.join(projectdir, "modules")

sys.path.insert(0, modulesdir)

import textdl
import json
import re
import requests
from bs4 import BeautifulSoup as bs
import time

# Selenium
from selenium import webdriver

# Chromedriver options
from selenium.webdriver.chrome.options import Options
chrome_options = Options()
chrome_options.add_argument("--disable-extensions")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--headless")

# Dirs
driver_path = os.path.join('C:/', 'chromedriver', 'chromedriver.exe')
#driver_path = os.path.join('/usr/lib/chromium-browser/chromedriver') # ubuntu
datapath = os.path.join('D:/', 'data',  'dk_news', 'articles_20210406')
outpath = os.path.join(datapath)

ber_inname = "berlingske_articles.json"
ber_outname = "berlingske_articles_with-text.json"
dr_inname = "dr_articles.json"
dr_outname = "dr_articles_with-text.json"
eb_inname = "eb_articles.json"
eb_outname = "eb_articles_with-text.json"
jp_inname = "jp_articles.json"
jp_outname = "jp_articles_with-text.json"
pol_inname = "politiken_articles.json"
pol_outname = "politiken_articles_with-text.json"
tv2_inname = "tv2_articles.json"
tv2_outname = "tv2_articles_with-text.json"

## Berlingske

with open(os.path.join(datapath, ber_inname), 'r', encoding = 'utf-8') as f:
    data = json.load(f)

for entry in data:
    entry['article_paywall'], entry['article_text'] = textdl.get_arttext(entry.get('article_link', driver_path = driver_path, source = "Berlingske", chrome_options = chrome_options))
    time.sleep(0.5)

with open(os.path.join(outpath, ber_outname), 'w', encoding = 'utf-8') as f:
    json.dump(data, f)

    
## DR

with open(os.path.join(datapath, dr_inname), 'r', encoding = 'utf-8') as f:
    data = json.load(f)

for entry in data:
    entry['article_paywall'], entry['article_text'] = textdl.get_arttext(entry.get('article_link', driver_path = driver_path, source = "DR", chrome_options = chrome_options))
    time.sleep(0.5)

with open(os.path.join(outpath, dr_outname), 'w', encoding = 'utf-8') as f:
    json.dump(data, f)

    
## EB

with open(os.path.join(datapath, eb_inname), 'r', encoding = 'utf-8') as f:
    data = json.load(f)

for entry in data:
    entry['article_paywall'], entry['article_text'] = textdl.get_arttext(entry.get('article_link', driver_path = driver_path, source = "EB", chrome_options = chrome_options))
    time.sleep(0.5)

with open(os.path.join(outpath, eb_outname), 'w', encoding = 'utf-8') as f:
    json.dump(data, f)

    
## JP

with open(os.path.join(datapath, jp_inname), 'r', encoding = 'utf-8') as f:
    data = json.load(f)

for entry in data:
    entry['article_paywall'], entry['article_text'] = textdl.get_arttext(entry.get('article_link', driver_path = driver_path, source = "JP", chrome_options = chrome_options))
    time.sleep(0.5)

with open(os.path.join(outpath, jp_outname), 'w', encoding = 'utf-8') as f:
    json.dump(data, f)

    
## Politiken

with open(os.path.join(datapath, pol_inname), 'r', encoding = 'utf-8') as f:
    data = json.load(f)

for entry in data:
    entry['article_paywall'], entry['article_text'] = textdl.get_arttext(entry.get('article_link', driver_path = driver_path, source = "Politiken", chrome_options = chrome_options))
    time.sleep(0.5)

with open(os.path.join(outpath, pol_outname), 'w', encoding = 'utf-8') as f:
    json.dump(data, f)

    
## TV2

with open(os.path.join(datapath, tv2_inname), 'r', encoding = 'utf-8') as f:
    data = json.load(f)

for entry in data:
    entry['article_paywall'], entry['article_text'] = textdl.get_arttext(entry.get('article_link', driver_path = driver_path, source = "TV2", chrome_options = chrome_options))
    time.sleep(0.5)

with open(os.path.join(outpath, tv2_outname), 'w', encoding = 'utf-8') as f:
    json.dump(data, f)