# Packages
import re
from bs4 import BeautifulSoup as bs
import time

def get_arttextfromraw(articlesource, newspaper):
    
    soup = bs(articlesource, 'html.parser')
    
    if newspaper == "DR":
        text = soup.find('div', class_ = "dre-article-body").get_text()

        return(text)
    
    elif newspaper == "Politiken":
        text = soup.find('div', class_ = "article__body").get_text()

        return(text)  
    
    elif newspaper == "Berlingske":
        text = soup.find('div', id = "articleBody").get_text()
            
        return(text)
        
    elif newspaper == "TV2":
        text = soup.find(attrs = {'data-adobe-context': 'article-body'}).get_text()

        return(text)
    
    elif newspaper == "EB":
        text = soup.find('div', class_ = "article-bodytext").get_text()

        return(text)
    
    elif newspaper == "JP":
        text = soup.find('article-body').get_text()

        return(text)