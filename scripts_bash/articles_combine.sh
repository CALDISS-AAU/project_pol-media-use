#!/bin/bash

source /home/ubuntu/anaconda3/etc/profile.d/conda.sh

conda activate mlbase

cd ~/data/dk-news/

rm articles_old/*

mv articles/* articles_old

mv latest_data/* old_data/

unzip polarticles_$(date +%F).zip -d articles/

cd ~

python ~/project_pol-media-use/scripts/articles_combine_json_csv.py