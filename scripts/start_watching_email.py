#!/usr/bin/env python

import os, sys
parentdir = os.path.dirname(os.path.dirname(os.path.realpath(__name__)))
modulesdir = os.path.join(parentdir, "modules")
import time
from datetime import datetime
from random import randint
sys.path.append(modulesdir)
import fp_watcher
import logging
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

logger = logging.getLogger(__name__)



def main():
    #Setting up e-mail notifications

    msg = MIMEMultipart()
    
    msg['From'] = 'kristian@mail.bot'
    msg['To'] = 'kgk@adm.aau.dk'
    msg['Subject'] = "Error running headline_watcher"
    
    #Setting up counter
    ARTICLE_COUNTER = {"DR": 0,
                   "Politiken": 0,
                   "Berlingske": 0, 
                   "TV2": 0}
    
    #Parameters for watch
    keywords = [r".*"]

    datadir = "../data/"

    end_time = datetime(2020, 12, 1)

    dt_now = datetime.now()
    
    sources = ["DR", "Politiken", "Berlingske", "TV2"]
    
    #Watch running
    while dt_now < end_time:
        s = smtplib.SMTP('smtp-relay.sendinblue.com', 587)
        s.starttls()
        s.login("kgk@adm.aau.dk", "a94Q187jgzb0vWEO")
        
        for source in sources:
            print("{time}: Checking {source} front page...".format(time = dt_now, source = source))
            logger.info("Checking {source} front page...".format(source = source))
            try:
                count = fp_watcher.headline_watch(source = source, keywords = keywords, datadir = datadir)
            except Exception as e:
                logger.error("Failed to run watch on {source}: ".format(source = source) + str(e))
                message = "<p><i>Watch on {source} was halted with the following error:</i> <br /> <br /> {error}".format(source = source, error = e)
                msg.attach(MIMEText(message, 'html'))
    
                s.send_message(msg)   
            
            if count == 0:
                ARTICLE_COUNTER[source] = ARTICLE_COUNTER[source] + 1
            else:
                ARTICLE_COUNTER[source] = 0
            
            if ARTICLE_COUNTER[source] >= 6:
                message = "<p><i>Warning: Watch on {source} has run {n} times with 0 new articles found</i></p>.".format(source = source, n = ARTICLE_COUNTER[source])
                msg.attach(MIMEText(message, 'html'))
                
                s.send_message(msg)
                
        s.quit()
        
        time_out = randint(41*60, 62*60)
        time.sleep(time_out)
    
        dt_now = datetime.now()
    

if __name__ == '__main__':
    FORMAT = '%(asctime)-15s %(message)s'
    logging.basicConfig(filename='./watcher.log', filemode='w', level=logging.INFO, format = FORMAT)
    main()
