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
from random import randint
from itertools import compress
import json
import logging

logger = logging.getLogger(__name__)

def keyword_check(keywords, headline):
    '''
    Checks whether headline contains keywords.
    '''
    text = headline.css("div ::text").getall()
    text = ' '.join(text)
    text = text.lower()
    if any(word in text for word in keywords):
        return True
    else:
        return False
    
def get_headline(headline_sel):
    '''
    Extracts the headline from a Selector object as text.
    '''
    headline = Selector(text = headline_sel.css("div:first-of-type").get()).css(' ::text').getall()
    headline = ''.join(headline)
    headline = headline.lower()
    headline = re.sub('\n', ' ', headline)
    headline = re.sub('\s\s', '', headline)
    headline = re.sub('\s\s', '', headline)
    return(headline)

def get_articlelink(headline_sel):
    '''
    Extracts the link to the article from the headline.
    '''
    link = headline_sel.css("::attr(href)").get()
    return(link)

def get_article_info(headline, keywords):
    '''
    Creates a dictionary of information from a headline.
    '''    
    i = 3
    
    art_uuid = str(uuid.uuid4())
    encounter_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
    
    frontpage_title = get_headline(headline)
    article_link = headline.css("::attr(href)").get()
    
    matches = list(compress(keywords, [keyword in frontpage_title for keyword in keywords]))
    
    while i > 0:
        time_out = randint(2, 5)
        time.sleep(time_out)
        response_code = requests.get(article_link, timeout = 5.0).status_code

        if response_code == 200:     

            info = dict()

            html = requests.get(article_link, timeout = 5.0).content
            sel = Selector(text = html)

            title_sel = "title ::text"
            datetime_xpath = '//meta[contains(@property,"article:published_time")]/@content'

            article_title = sel.css(title_sel).get()
            article_datetime = sel.xpath(datetime_xpath).get()

            info['uuid'] = art_uuid
            info['article_accessed'] = 1
            info['newspaper_name'] = 'Berlingske'
            info['newspaper_frontpage_url'] = 'https://www.berlingske.dk/'
            info['frontpage_selector'] = "div.front.theme-berlingske"
            info['keywords_search'] = keywords
            info['keywords_match'] = matches
            info['article_title'] = article_title
            info['frontpage_title'] = frontpage_title
            info['article_link'] = article_link
            info['article_datetime'] = article_datetime
            info['encounter_datetime'] = encounter_time
            return(info)
        else:
            i = i -1
        
        if i == 0:
            
            info = dict()
            
            info['uuid'] = art_uuid
            info['article_accessed'] = 0
            info['newspaper_name'] = 'Berlingske'
            info['newspaper_frontpage_url'] = 'https://www.berlingske.dk/'
            info['frontpage_selector'] = "div.front.theme-berlingske"
            info['keywords_search'] = keywords
            info['keywords_match'] = matches
            info['article_title'] = ''
            info['frontpage_title'] = frontpage_title
            info['article_link'] = article_link
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
    sel = Selector(text = html)

    #selector of top frontpage contet
    front_sel = "div.front.theme-berlingske"
    front_page = sel.css(front_sel)

    #get headline selectors
    headline_xpath = '//article/div/a[contains(@class,"dre-item")]'
    headlines = front_page.xpath(headline_xpath)

    #extract headlines based on keyword
    headlines_ext = list()

    for headline in headlines:
        if keyword_check(keywords, headline) == True:
            headlines_ext.append(headline)
    
    #get article info
    articles = []

    for headline in headlines_ext:
        link = get_articlelink(headline)
        if not link in url_list:
            art_info = get_article_info(headline, keywords = keywords)
            articles.append(art_info)
            url_list.append(link)
    
    return(articles)


def headline_watch(keywords, datadir, main_url = 'https://www.berlingske.dk/'):
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
            
            print("Berlingske front page checked on {time}. {n} new articles found.".format(time = datetime.datetime.now(), n = len(articles)))
            logger.info("Berlingske front page checked on {time}. {n} new articles found.".format(time = datetime.datetime.now(), n = len(articles)))
            return
    else:
        print("Error retrieving Berlingske front page on {time}. Skipping...".format(time = datetime.datetime.now()))
        logger.warning("Error retrieving Berlingske front page on {time}. Skipping...".format(time = datetime.datetime.now()))
        return       
