#!/bin/bash

source /home/ubuntu/anaconda3/etc/profile.d/conda.sh

cd ~/data/poltweets/

mv tweets/* tweets_old

mv latest_data/*.gz old_data/

unzip poltweets_$(date +%F).zip -d tweets/

python project_pol-media-use/scripts/tweets_combine.py

python project_pol-media-use/scripts/tweets_wrangle.py