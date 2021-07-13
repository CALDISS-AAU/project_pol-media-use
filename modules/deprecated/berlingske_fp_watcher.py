from bs4 import BeautifulSoup as bs

import scrapy
import requests
from scrapy import Selector

import os
import sys
import datetime

import re
import time
import uuid
import random
from random import randint
from itertools import compress
import json
import logging

logger = logging.getLogger(__name__)

def keyword_check(keywords, headline):
    '''
    Checks whether headline contains keywords.
    '''
    text = headline.get_text().lower()
    if any(re.match(word, text) for word in keywords):
        return True
    else:
        return False

def get_article_info(link, keywords, source_url = "https://www.berlingske.dk/nyheder/politik"):
    '''
    Creates a dictionary of information from a headline.
    '''    
    i = 3
    
    art_uuid = str(uuid.uuid4())
    encounter_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
    
    while i > 0:
        time_out = randint(2, 5)
        time.sleep(time_out)
        req = requests.get(link, timeout = 5.0)
        response_code = req.status_code

        if response_code == 200:     

            info = dict()

            html = requests.get(link, timeout = 5.0).content
            sel = Selector(text = html)

            title_sel = "title ::text"
            datetime_xpath = '//meta[contains(@property,"article:published_time")]/@content'

            article_title = sel.css(title_sel).get()
            article_datetime = sel.xpath(datetime_xpath).get()
            
            matches = list(compress(keywords, [keyword in article_title.lower() for keyword in keywords]))
            
            info['uuid'] = art_uuid
            info['article_accessed'] = 1
            info['newspaper_name'] = 'Berlingske'
            info['newspaper_frontpage_url'] = source_url
            info['keywords_search'] = keywords
            info['keywords_match'] = matches
            info['article_title'] = article_title
            info['article_link'] = link
            info['article_datetime'] = article_datetime
            info['encounter_datetime'] = encounter_time
            info['article_source'] = str(bs(req.content, "html.parser"))
            
            return(info)
        else:
            i = i -1
        
        if i == 0:
            
            info = dict()
            
            info['uuid'] = art_uuid
            info['article_accessed'] = 0
            info['newspaper_name'] = 'Berlingske'
            info['newspaper_frontpage_url'] = source_url
            info['keywords_search'] = keywords
            info['keywords_match'] = matches
            info['article_title'] = ''
            info['article_link'] = link
            info['article_datetime'] = ''
            info['encounter_datetime'] = encounter_time
            info['article_source'] = ''
            
            return(info)

def front_page_check(url, keywords, url_list):
    '''
    Creates dictionary of headlines with various information.
    '''
    #selector of main page
    url = url
    html = requests.get(url, timeout = 5.0).content
    soup = bs(html, "html.parser")
    
    #get headline soups
    headlines = soup.find_all("a", class_=re.compile("teaser__title-link"))

    #extract headlines based on keyword
    headlines_ext = list()

    for headline in headlines:
        if keyword_check(keywords, headline) == True:
            headlines_ext.append(headline)

    #get links from extracted headlines
    links_ext = list()
    for headline in headlines_ext:
        link = "https://www.berlingske.dk" + headline['href']
        links_ext.append(link)
    links_ext = list(filter(None, links_ext))
    
    #get article info
    articles = []

    for link in links_ext:
        if not link in url_list:
            art_info = get_article_info(link, keywords = keywords)
            articles.append(art_info)
            url_list.append(link)
            time_out = random.uniform(0.5, 2.0)
            time.sleep(time_out)
            
    return(articles)


def headline_watch(keywords, datadir, source_url = 'https://www.berlingske.dk/nyheder/politik/'):
    '''
    Checks the frontpage and stores info about headlines matching keywords.
    '''
    keywords = keywords
    
    urldir = datadir + "urls/"
    
    urllist_filename = "berlingske_article_urls.txt"
    
    data_filename = "berlingske_articles.json"
    
    url_list = []
    
    try:
        with open(urldir + urllist_filename, 'r') as f:
            for line in f:
                url_list.append(line.strip())
            f.close()
    except IOError:
        print("No existing url list. Creating new file {}".format(urllist_filename))
        logger.info("No existing url list. Creating new file {}".format(urllist_filename))
        if not os.path.isdir(urldir):
            os.mkdir(urldir)

    try:
        with open(datadir + data_filename, 'r') as f:
            f.close()
    except IOError:
        print("No existing data file. Creating new file {}".format(data_filename))
        logger.info("No existing data file. Creating new file {}".format(data_filename))
        with open(datadir + data_filename, 'w') as f:
            json.dump([], f)

    i = 3
    
    while i > 0:
        try:
            response = requests.get(source_url, timeout = 5.0)
            break
        except:
            i = i - 1
            time_int = random.uniform(0.1, 0.2) 
            time.sleep(time_int)
            continue
    
    if i > 0: 
        if response.status_code == 200:
            articles = front_page_check(url = source_url, keywords = keywords, url_list = url_list)

            if len(articles) != 0:
                with open(datadir + data_filename, 'r') as f:
                    heads = json.load(f)
                    heads = heads + articles
                    f.close()
                with open(datadir + data_filename, 'w') as file:
                    json.dump(heads, file)
                file.close()

            for article in articles:
                url_list.append(article['article_link'])
            
            url_list = list(set(url_list))

            with open(urldir + urllist_filename, 'w') as f:
                for url in url_list:
                    f.write(url + "\n")
                f.close()
            
            print("Berlingske front page checked on {time}. {n} new articles found.".format(time = datetime.datetime.now(), n = len(articles)))
            logger.info("Berlingske front page checked on {time}. {n} new articles found.".format(time = datetime.datetime.now(), n = len(articles)))
            return
    else:
        print("Error retrieving Berlingske front page on {time}. Skipping...".format(time = datetime.datetime.now()))
        logger.warning("Error retrieving Berlingske front page on {time}. Skipping...".format(time = datetime.datetime.now()))
        return       
