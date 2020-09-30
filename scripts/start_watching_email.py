import sys
import time
from datetime import datetime
from random import randint
sys.path.append('../modules')
import berlingske_fp_watcher as berwatch
import politiken_fp_watcher as polwatch
import dr_fp_watcher as drwatch
import logging
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

logger = logging.getLogger(__name__)

def main():
    #Setting up e-mail notifications
    s = smtplib.SMTP('smtp-relay.sendinblue.com', 587)

    msg = MIMEMultipart()
    
    msg['From'] = 'kristian@mail.bot'
    msg['To'] = 'kgk@adm.aau.dk'
    msg['Subject'] = "Error running headline_watcher"
    
    #Parameters for watch
    keywords = ['klima', 'miljø', 'klimalov', 'grøn', 'bæredygtig', 'fossil', 'olie']

    datadir = "../data/"

    end_time = datetime(2020, 8, 17)

    dt_now = datetime.now()
    
    #Watch running
    while dt_now < end_time:
        s.starttls()
        s.login("kgk@adm.aau.dk", "a94Q187jgzb0vWEO")
        
        print("{time}: Checking Berlingske front page...".format(time = dt_now))
        logger.info("Checking Berlingske front page...")
        try:
            berwatch.headline_watch(keywords = keywords, datadir = datadir)
        except Exception as e:
            logger.error("Failed to run watch on Berlingske: " + str(e))
            message = "<p><i>Watch on Berlingske was halted with the following error:</i> <br /> <br /> {error}".format(error = e)
            msg.attach(MIMEText(message, 'html'))

            s.send_message(msg)   
            
    
        print("{time}: Checking Politiken front page...".format(time = dt_now))
        logger.info("Checking Politiken front page...")
        try:
            polwatch.headline_watch(keywords = keywords, datadir = datadir)
        except Exception as e:
            logger.error("Failed to run watch on Politiken: " + str(e))
            message = "<p><i>Watch on Politiken was halted with the following error:</i> <br /> <br /> {error}".format(error = e)
            msg.attach(MIMEText(message, 'html'))

            s.send_message(msg)   
        
        print("{time}: Checking DR front page...".format(time = dt_now))
        logger.info("Checking DR front page...")
        try:
            drwatch.headline_watch(keywords = keywords, datadir = datadir)
        except Exception as e:
            logger.error("Failed to run watch on DR: " + str(e))
            message = "<p><i>Watch on DR was halted with the following error:</i> <br /> <br /> {error}".format(error = e)
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