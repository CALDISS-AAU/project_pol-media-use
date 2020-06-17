import sys
import time
from datetime import datetime
from random import randint
sys.path.append('../modules')
import berlingske_fp_watcher as berwatch
import politiken_fp_watcher as polwatch


keywords = ['klima', 'miljø', 'klimalov', 'grøn', 'bæredygtig', 'fossil', 'olie']

datadir = "../data/"

end_time = datetime(2020, 7, 1)

dt_now = datetime.now()

while dt_now < end_time:
	print("{time}: Checking Berlingske front page...".format(time = dt_now))
    berwatch.headline_watch(keywords = keywords, datadir = datadir)
	
	print("{time}: Checking Politiken front page...".format(time = dt_now))
	polwatch.headline_watch(keywords = keywords, datadir = datadir)
	
    time_out = randint(41*60, 62*60)
    time.sleep(time_out)
	
	dt_now = datetime.now()