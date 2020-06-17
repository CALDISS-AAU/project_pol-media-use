import sys
import time
from datetime import datetime
from random import randint
sys.path.append('../modules')
import berlingske_fp_watcher as fpwatch

keywords = ['klima', 'miljø', 'klimalov', 'grøn', 'bæredygtig', 'fossil', 'olie']

datadir = "../data/"

end_time = datetime(2020, 7, 1)

dt_now = datetime.now()

while dt_now < end_time:
    fpwatch.headline_watch(keywords = keywords, datadir = datadir)
	
    time_out = randint(41*60, 62*60)
    time.sleep(time_out)
	
	dt_now = datetime.now()