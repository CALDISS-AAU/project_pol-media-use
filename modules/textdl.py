# Packages
import re
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

def get_arttext(link, driver_path, source, chrome_options = chrome_options):
    driver = webdriver.Chrome(executable_path = driver_path, options=chrome_options)

    driver.get(link)
    time.sleep(0.5)
    pageSource = driver.page_source.encode("utf-8")
    driver.quit()

    soup = bs(pageSource, 'html.parser')
    
    if source == "DR":
        paywall = False
        text = soup.find('div', class_ = "dre-article-body").get_text()

        return(paywall, text)
    
    elif source == "Politiken":
        if soup.find(class_ = "stopsign"):
            paywall = True
            text = ''
        else:
            paywall = False
            text = soup.find('div', class_ = "article__body").get_text()

        return(paywall, text)        
    
    elif source == "Berlingske"
        if soup.find(class_ = "paywall"):
            paywall = True
            text = ''
        else:
            paywall = False
            text = soup.find('div', id = "articleBody").get_text()
            
        return(paywall, text)
        
    elif source == "TV2":
        paywall = False
        text = soup.find(attrs = {'data-adobe-context': 'article-body'}).get_text()

        return(paywall, text)    
    
    elif source == "EB":
        if soup.find(class_ = re.compile(r'paywall')):
            paywall = True
            text = ''
        else:
            paywall = False
            text = soup.find('div', class_ = "article-bodytext").get_text()

        return(paywall, text) 
    
    elif source == "JP":
        paywall = False
        text = soup.find('article-body').get_text()

        return(paywall, text)        