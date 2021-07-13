#!/bin/bash

rm ~/poltweets_zipped/*.zip

mkdir poltweets_cp

cp --parents -rp twitter-users/data/*/tweets/ poltweets_cp/

cd poltweets_cp/twitter-users/data

for d in *; do
  [[ -d "$d" ]] && cd "$d/tweets" || continue
  for f in 2*.ndjson; do mv -- "${f}" "${d}_${f}" ;
  done
  cd -
done

cd ~

mkdir poltweets_cp/tweets
mv poltweets_cp/twitter-users/data/*/tweets/*.ndjson poltweets_cp/tweets

cd ./poltweets_cp/tweets/
rm [0-9]*.ndjson

zip -r ~/poltweets_zipped/poltweets_$(date +%F).zip *.ndjson

cd ~

scp ~/poltweets_zipped/poltweets_$(date +%F).zip ubuntu@130.226.98.145:data/poltweets/

rm -r poltweets_cp