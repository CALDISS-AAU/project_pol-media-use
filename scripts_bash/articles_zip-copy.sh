#!/bin/bash

mkdir articles_cp

cp ~/project_pol-media-use/data/articles/*.json articles_cp/

cd articles_cp/

zip -r ~/articles_zipped/polarticles_$(date +%F).zip *.json

cd ~

scp ~/articles_zipped/polarticles_$(date +%F).zip ubuntu@130.226.98.145:data/dk-news/

rm -r articles_cp