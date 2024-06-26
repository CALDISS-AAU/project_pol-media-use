#!/bin/bash

source /home/ubuntu/anaconda3/etc/profile.d/conda.sh

conda activate mlbase

cd ~/data/poltweets/

rm tweets_old/*

mv tweets/* tweets_old

mv latest_data/*.gz old_data/

unzip poltweets_$(date +%F).zip -d tweets/

cd ~

python ~/project_pol-media-use/scripts/tweets_combine.py

python ~/project_pol-media-use/scripts/tweets_wrangle.py