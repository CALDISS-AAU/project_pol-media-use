import os, sys
parentdir = os.path.dirname(os.path.dirname(os.path.realpath(__name__)))
modulesdir = os.path.join(parentdir, "modules")
import time
from datetime import datetime
from random import randint
sys.path.append(modulesdir)
import berlingske_fp_watcher as berwatch
import politiken_fp_watcher as polwatch
import dr_fp_watcher as drwatch
import tv2_fp_watcher as tv2watch
import logging
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

logger = logging.getLogger(__name__)

keywords = [r".*"]

datadir = "../data/testing/"

tv2watch.headline_watch(keywords = keywords, datadir = datadir)

