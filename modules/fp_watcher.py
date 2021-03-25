from bs4 import BeautifulSoup as bs

import requests
from urllib.parse import urljoin

import os
from datetime import datetime

import re
import time
import uuid
import random
from random import randint
from itertools import compress
import json
import logging

logger = logging.getLogger(__name__)

PARAMS = {"DR": {"url": "https://www.dr.dk/nyheder/politik/",
                 "heading_tag": "a",
                 "heading_class_regex": "dre-teaser-title*"}, 
          "Politiken": {"url": "https://politiken.dk/indland/politik/",
                        "heading_tag":"h2",
                        "heading_class_regex": "article-intro__title headline*"},
          "Berlingske": {"url": "https://www.berlingske.dk/nyheder/politik/",
                         "heading_tag": "a", 
                         "heading_class_regex": "teaser__title-link"},
          "TV2": {"url": "https://nyheder.tv2.dk/politik/",
                  "heading_tag": "a",
                  "heading_class_regex": "o-teaser_link"},
          "EB": {"url": "https://ekstrabladet.dk/nyheder/politik/",
                 "heading_tag": "a",
                 "heading_class_regex": "card"},
          "JP": {"url": "https://jyllands-posten.dk/politik/",
                 "heading_tag": "a",
                 "heading_class_regex": "article-teaser-heading"}
                }

SOURCES = tuple(PARAMS.keys())

def get_title(soup):
    try:
        article_title = soup.title.get_text()
    except:
        article_title = ""
        
    return(article_title)


def get_datetime(soup):
    try:
        article_datetime = soup.find("meta", attrs={"name": "article:published_time"})['content']
    except (TypeError, KeyError):
        try:
            article_datetime = soup.find("meta", attrs={'property': re.compile('article:published_time')})['content']
        except:
            article_datetime = ""

    return(article_datetime)


def get_links_dr(headlines):
    links = list()
    for headline in headlines:
        try:
            link = urljoin("https://www.dr.dk", headline['href'])
            links.append(link)
        except:
            continue
    links = list(filter(None, links))
    links = list(set(links))
    
    return(links)


def get_links_pol(headlines):
    links = list()
    for headline in headlines:
        try:
            link = urljoin("https://politiken.dk", headline.a['href'])
            links.append(link)
        except:
            continue
    links = list(filter(None, links))
    links = list(set(links))
    
    return(links)


def get_links_ber(headlines):
    links = list()
    for headline in headlines:
        try:
            link = urljoin("https://www.berlingske.dk", headline['href'])
            links.append(link)
        except:
            continue
    links = list(filter(None, links))
    links = list(set(links))
    
    return(links)


def get_links_tv2(pagesoup, page_params, keywords = [r".*"]):
    
    # extract relevant sections soups
    section_soups = pagesoup.find_all('section', class_ = "g-gutter")
    div_soups = []
    for section_soup in section_soups[0:2]:
        div_soup = section_soup.find('div')
        div_soups.append(div_soup)

    div_soups.append(section_soups[2])

    #get headline soups
    headlines = []
    for div_soup in div_soups:
        div_headlines = div_soup.find_all(page_params['TV2']['heading_tag'], class_ = re.compile(page_params['TV2']['heading_class_regex']))
        headlines = headlines + div_headlines

    #extract headlines based on keyword
    headlines_ext = list()

    for headline in headlines:
        if keyword_check(keywords, headline) == True:
            headlines_ext.append(headline)
       
    links = list()
    for headline in headlines_ext:
        try:
            link = urljoin("https://nyheder.tv2.dk/", headline['href'])
            links.append(link)
        except:
            continue
    links = list(filter(None, links))
    links = list(set(links))
    
    return(links)


def get_links_eb(pagesoup, page_params, keywords = [r".*"]):
    section_soup = pagesoup.find('div', class_ = 'flex flex-wrap--wrap flex-justify--between') 
    
    #get headline soups
    headlines = section_soup.find_all(page_params['heading_tag'], class_=re.compile(page_params['heading_class_regex']))

    #extract headlines based on keyword
    headlines_ext = list()

    for headline in headlines:
        if keyword_check(keywords, headline) == True:
            headlines_ext.append(headline)
       
    links = list()
    for headline in headlines_ext:
        try:
            link = urljoin("https://ekstrabladet.dk/", headline['href'])
            links.append(link)
        except:
            continue
    links = list(filter(None, links))
    links = list(set(links))
    
    return(links)
        
def get_links_jp(pagesoup, page_params, keywords = [r".*"]):
    section_soup = pagesoup.find('section', id = 'section_a_zone_3')
    
    #get headline soups
    headlines = section_soup.find_all(page_params['heading_tag'], class_=re.compile(page_params['heading_class_regex']))

    #extract headlines based on keyword
    headlines_ext = list()

    for headline in headlines:
        if keyword_check(keywords, headline) == True:
            headlines_ext.append(headline)
       
    links = list()
    for headline in headlines_ext:
        try:
            link = urljoin("https://jyllands-posten.dk/", headline['href'])
            links.append(link)
        except:
            continue
    links = list(filter(None, links))
    links = list(set(links))
    
    return(links)
    
def keyword_check(keywords, headline):
    '''
    Checks whether headline contains keywords.
    '''
    text = headline.get_text().lower()
    if any(re.match(word, text) for word in keywords):
        return True
    else:
        return False
    
def get_article_info(link, keywords, source, source_url, get_source = False):
    '''
    Creates a dictionary of information from a headline.
    '''
    i = 3
    
    art_uuid = str(uuid.uuid4())
    encounter_time = datetime.now().strftime('%Y-%m-%d %H:%M')
    
    while i > 0:
        time_out = random.uniform(1, 2)
        time.sleep(time_out)
        req = requests.get(link, timeout = 5.0)
        response_code = req.status_code

        if response_code == 200:     

            info = dict()

            html = requests.get(link, timeout = 5.0).content
            soup = bs(html, "html.parser")

            article_title = get_title(soup)
            article_datetime = get_datetime(soup)

            matches = list(compress(keywords, [keyword in article_title.lower() for keyword in keywords]))

            info['uuid'] = art_uuid
            info['article_accessed'] = 1
            info['newspaper_name'] = source
            info['newspaper_frontpage_url'] = source_url
            info['keywords_search'] = keywords
            info['keywords_match'] = matches
            info['article_title'] = article_title
            info['article_link'] = link
            info['article_datetime'] = article_datetime
            info['encounter_datetime'] = encounter_time
            if get_source:
                info['article_source'] = str(bs(req.content, "html.parser"))
            else:
                info['article_source'] = ''
            return(info)
        else:
            i = i -1
        
        if i == 0:
            
            info = dict()
            
            info['uuid'] = art_uuid
            info['article_accessed'] = 0
            info['newspaper_name'] = source
            info['newspaper_frontpage_url'] = source_url
            info['keywords_search'] = keywords
            info['keywords_match'] = ''
            info['article_title'] = ''
            info['article_link'] = link
            info['article_datetime'] = ''
            info['encounter_datetime'] = encounter_time
            info['article_source'] = ''
            return(info)

def front_page_check(source, keywords, url_list, get_source = False):
    '''
    Creates dictionary of headlines with various information.
    '''    
    #get parameters
    if source not in SOURCES:
        raise Exception("{source} is not a valid source. Valid sources are {sources}.".format(source = source, sources = re.sub(r'\(|\)', '', str(SOURCES))))
        
    page_params = PARAMS[source]
    
    #selector of main page
    url = page_params['url']
    html = requests.get(url, timeout = 5.0).content
    soup = bs(html, "html.parser")

    #get headline soups
    headlines = soup.find_all(page_params['heading_tag'], class_=re.compile(page_params['heading_class_regex']))

    #extract headlines based on keyword
    headlines_ext = list()

    for headline in headlines:
        if keyword_check(keywords, headline) == True:
            headlines_ext.append(headline)

    #get links from extracted headlines
    if source == "DR":
        links_ext = get_links_dr(headlines_ext)
    elif source == "Politiken":
        links_ext = get_links_pol(headlines_ext)
    elif source == "Berlingske":
        links_ext = get_links_ber(headlines_ext)
    elif source == "TV2":
        links_ext = get_links_tv2(soup, page_params, keywords = keywords)
    elif source == "EB":
        links_ext = get_links_eb(soup, page_params, keywords = keywords)
    elif source == "JP":
        links_ext = get_links_jp(soup, page_params, keywords = keywords)

    #get article info
    articles = []

    for link in links_ext:
        if not link in url_list:
            art_info = get_article_info(link = link, keywords = keywords, source = source, source_url = page_params['url'], get_source = get_source)
            articles.append(art_info)
            url_list.append(link)
            
    return(articles)

def headline_watch(source, keywords, datadir, get_source = False):
    '''
    Checks the frontpage and stores info about headlines matching keywords.
    '''
    
    #get parameters
    if source not in SOURCES:
        raise Exception("{source} is not a valid source. Valid sources are {sources}.".format(source = source, sources = re.sub(r'\(|\)', '', str(SOURCES))))
        
    page_params = PARAMS[source]
    
    
    keywords = keywords
    
    source_url = page_params['url']
    
    urldir = os.path.join(datadir, "urls")
    
    articlesdir = os.path.join(datadir, "articles")

    urllist_filename = source.lower() + "_article_urls.txt"

    data_filename = source.lower() + "_articles.json"

    url_list = []

    try:
        with open(os.path.join(urldir, urllist_filename), 'r') as f:
            for line in f:
                url_list.append(line.strip())
            f.close()
    except IOError:
        print("No existing url list. Creating new file {}".format(urllist_filename))
        logger.info("No existing url list. Creating new file {}".format(urllist_filename))
        if not os.path.isdir(urldir):
            os.mkdir(urldir)

    try:
        with open(os.path.join(articlesdir, data_filename), 'r') as f:
            f.close()
    except IOError:
        print("No existing data file. Creating new file {}".format(data_filename))
        logger.info("No existing data file. Creating new file {}".format(data_filename))
        if not os.path.isdir(articlesdir):
            os.mkdir(articlesdir)
        with open(os.path.join(articlesdir, data_filename), 'w') as f:
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
            articles = front_page_check(source = source, keywords = keywords, url_list = url_list, get_source = get_source)

            if len(articles) != 0:
                with open(os.path.join(articlesdir, data_filename), 'r') as f:
                    heads = json.load(f)
                    heads = heads + articles
                    f.close()
                with open(os.path.join(articlesdir, data_filename), 'w') as file:
                    json.dump(heads, file)
                file.close()

            for article in articles:
                url_list.append(article['article_link'])

            url_list = list(set(url_list))

            with open(os.path.join(urldir, urllist_filename), 'w') as f:
                for url in url_list:
                    f.write(url + "\n")
                f.close()

            print("{source} front page checked on {time}. {n} new articles found.".format(source = source, time = datetime.now(), n = len(articles)))
            logger.info("{source} front page checked on {time}. {n} new articles found.".format(source = source, time = datetime.now(), n = len(articles)))
            return(len(articles))
    else:
        print("Error retrieving {source} front page on {time}. Skipping...".format(source = source, time = datetime.now()))
        logger.warning("Error retrieving {source} front page on {time}. Skipping...".format(source = source, time = datetime.now()))      
        return(0)