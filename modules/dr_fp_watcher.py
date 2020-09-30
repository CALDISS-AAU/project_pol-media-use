from bs4 import BeautifulSoup as bs

import requests

import os
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
    if any(word in text for word in keywords):
        return True
    else:
        return False

def get_article_info(link, keywords):
    '''
    Creates a dictionary of information from a headline.
    '''
    i = 3
    
    art_uuid = str(uuid.uuid4())
    encounter_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
    
    while i > 0:
        time_out = randint(2, 5)
        time.sleep(time_out)
        response_code = requests.get(link, timeout = 5.0).status_code

        if response_code == 200:     

            info = dict()

            html = requests.get(link, timeout = 5.0).content
            soup = bs(html, "html.parser")

            article_title = soup.title.get_text()
            try:
                article_datetime = soup.time['datetime']
            except TypeError:
                article_datetime = ''

            matches = list(compress(keywords, [keyword in article_title.lower() for keyword in keywords]))

            info['uuid'] = art_uuid
            info['article_accessed'] = 1
            info['newspaper_name'] = 'DR Nyheder'
            info['newspaper_frontpage_url'] = 'https://www.dr.dk/nyheder/indland'
            info['frontpage_selector'] = "div.dre-container dre-container--margin-top"
            info['keywords_search'] = keywords
            info['keywords_match'] = matches
            info['article_title'] = article_title
            info['article_link'] = link
            info['article_datetime'] = article_datetime
            info['encounter_datetime'] = encounter_time
            return(info)
        else:
            i = i -1
        
        if i == 0:
            
            info = dict()
            
            info['uuid'] = art_uuid
            info['article_accessed'] = 0
            info['newspaper_name'] = 'DR Nyheder'
            info['newspaper_frontpage_url'] = 'https://www.dr.dk/nyheder/indland'
            info['frontpage_selector'] = "div.dre-container dre-container--margin-top"
            info['keywords_search'] = keywords
            info['keywords_match'] = ''
            info['article_title'] = ''
            info['article_link'] = link
            info['article_datetime'] = ''
            info['encounter_datetime'] = encounter_time
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
    headlines = soup.find_all("a", class_=re.compile("dre-teaser-title*"))

    #extract headlines based on keyword
    headlines_ext = list()

    for headline in headlines:
        if keyword_check(keywords, headline) == True:
            headlines_ext.append(headline)

    #get links from extracted headlines
    links_ext = list()
    for headline in headlines_ext:
        link = "https://www.dr.dk" + headline['href']
        links_ext.append(link)
    links_ext = list(filter(None, links_ext))
    links_ext = list(set(links_ext))

    #get article info
    articles = []

    for link in links_ext:
        if not link in url_list:
            print("accessing..." + link)
            art_info = get_article_info(link = link, keywords = keywords)
            articles.append(art_info)
            url_list.append(link)
            
    return(articles)

def headline_watch(keywords, datadir, main_url = 'https://www.dr.dk/nyheder/indland'):
    '''
    Checks the frontpage and stores info about headlines matching keywords.
    '''
    keywords = keywords

    urldir = datadir + "urls/"

    urllist_filename = "dr_article_urls.txt"

    data_filename = "dr_articles.json"

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
            response = requests.get(main_url, timeout = 5.0)
            break
        except:
            i = i - 1
            time_int = random.uniform(0.1, 0.2) 
            time.sleep(time_int)
            continue

    if i > 0: 
        if response.status_code == 200:
            articles = front_page_check(url = main_url, keywords = keywords, url_list = url_list)

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

            print("DR front page checked on {time}. {n} new articles found.".format(time = datetime.datetime.now(), n = len(articles)))
            logger.info("DR front page checked on {time}. {n} new articles found.".format(time = datetime.datetime.now(), n = len(articles)))
            return
    else:
        print("Error retrieving DR front page on {time}. Skipping...".format(time = datetime.datetime.now()))
        logger.warning("Error retrieving DR front page on {time}. Skipping...".format(time = datetime.datetime.now()))      
        return