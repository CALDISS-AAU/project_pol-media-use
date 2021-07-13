#!/bin/bash

# Run scripts to combine?
## Both a combined json and a zipped csv
## Filter based on latest article_accessed date in new data and combine

source /home/ubuntu/anaconda3/etc/profile.d/conda.sh

conda activate mlbase

cd ~/data/dk-news/

rm articles_old/*

mv articles/* articles_old

mv latest_data/* old_data/

unzip polarticles_$(date +%F).zip -d articles/

cd ~

# Scripts