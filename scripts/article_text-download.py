#!/usr/bin/env python
# coding: utf-8

# Packages
import json
import os
import re
import requests
from bs4 import BeautifulSoup as bs
import time

# Selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException, WebDriverException, ElementNotInteractableException
from selenium.webdriver.common.action_chains import ActionChains

# Chromedriver options
from selenium.webdriver.chrome.options import Options
chrome_options = Options()
chrome_options.add_argument("--disable-extensions")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--headless")

# Dirs
driver_path = os.path.join('C:/', 'chromedriver', 'chromedriver.exe')
datapath = os.path.join('D:/', 'data',  'dk_news', 'articles_20210406')
outpath = os.path.join(datapath, 'articles_with-text_20210406.json')


## Load data

datafiles = [os.path.join(datapath,f) for f in os.listdir(datapath) if os.path.isfile(os.path.join(datapath, f))]
datafiles = [datafile for datafile in datafiles if re.match(r'.*\.json', datafile)]

data = list()

for datafile in datafiles:
    with open(datafile, 'r', encoding = 'utf-8') as f:
        entries = json.load(f)
        data = data + entries


## Functions

def get_arttext_ber(link):
    driver = webdriver.Chrome(executable_path = driver_path, options=chrome_options)

    driver.get(link)
    pageSource = driver.page_source.encode("utf-8")
    driver.quit()

    soup = bs(pageSource, 'html.parser')
    
    if soup.find(class_ = "paywall"):
        paywall = True
        text = ''
    else:
        paywall = False
        text = soup.find('div', id = "articleBody").get_text()
    
    return(paywall, text)


def get_arttext_pol(link):
    driver = webdriver.Chrome(executable_path = driver_path, options=chrome_options)

    driver.get(link)
    pageSource = driver.page_source.encode("utf-8")
    driver.quit()

    soup = bs(pageSource, 'html.parser')
    
    if soup.find(class_ = "stopsign"):
        paywall = True
        text = ''
    else:
        paywall = False
        text = soup.find('div', class_ = "article__body").get_text()
    
    return(paywall, text)


def get_arttext_dr(link):
    # Undgå "engagement" links
    
    if "nyheder/politik/" not in link:
        return(None, None)
    
    driver = webdriver.Chrome(executable_path = driver_path, options=chrome_options)

    driver.get(link)
    pageSource = driver.page_source.encode("utf-8")
    driver.quit()

    soup = bs(pageSource, 'html.parser')
    
    paywall = False
    text = soup.find('div', class_ = "dre-article-body").get_text()
    
    return(paywall, text)


def get_arttext_eb(link):
    
    driver = webdriver.Chrome(executable_path = driver_path, options=chrome_options)

    driver.get(link)
    pageSource = driver.page_source.encode("utf-8")
    driver.quit()

    soup = bs(pageSource, 'html.parser')
    
    if soup.find(class_ = re.compile(r'paywall')):
        paywall = True
        text = ''
    else:
        paywall = False
        text = soup.find('div', class_ = "article-bodytext").get_text()
    
    return(paywall, text)


def get_arttext_jp(link):
    
    driver = webdriver.Chrome(executable_path = driver_path, options=chrome_options)

    driver.get(link)
    time.sleep(0.5)
    pageSource = driver.page_source.encode("utf-8")
    driver.quit()

    soup = bs(pageSource, 'html.parser')
    
    paywall = False
    text = soup.find('article-body').get_text()
    
    return(paywall, text)


def get_arttext_tv2(link):

    if "nyheder.tv2" not in link:
        return(None, None)    
    
    driver = webdriver.Chrome(executable_path = driver_path, options=chrome_options)

    driver.get(link)
    time.sleep(0.5)
    pageSource = driver.page_source.encode("utf-8")
    driver.quit()

    soup = bs(pageSource, 'html.parser')
    
    paywall = False
    text = soup.find(attrs = {'data-adobe-context': 'article-body'}).get_text()
    
    return(paywall, text)


for c, entry in enumerate(data, start = 1):
    if entry.get('newspaper_name' == 'TV2'):
        entry['article_paywall'], entry['article_text'] = get_arttext_tv2(entry.get('article_link'))
    elif entry.get('newspaper_name' == 'Berlingske'):
        entry['article_paywall'], entry['article_text'] = get_arttext_ber(entry.get('article_link'))
    elif entry.get('newspaper_name' == 'Politiken'):
        entry['article_paywall'], entry['article_text'] = get_arttext_pol(entry.get('article_link'))
    elif entry.get('newspaper_name' == 'DR'):
        entry['article_paywall'], entry['article_text'] = get_arttext_dr(entry.get('article_link'))    
    elif entry.get('newspaper_name' == 'EB'):
        entry['article_paywall'], entry['article_text'] = get_arttext_eb(entry.get('article_link'))  
    elif entry.get('newspaper_name' == 'JP'):
        entry['article_paywall'], entry['article_text'] = get_arttext_jp(entry.get('article_link'))  
    
    progress = "|{0}| {1:.2f} %".format(("="*int(c/len(data) * 50)).ljust(50), c/len(data) * 100)
    print(progress, end = "\r")
    
    time.sleep(0.5)


with open(outpath, 'w', encoding = 'utf-8') as f:
    json.dump(data, f)

