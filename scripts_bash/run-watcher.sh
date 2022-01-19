#!/bin/bash

source /home/ubuntu/anaconda3/etc/profile.d/conda.sh
conda activate webwatch

python "/home/ubuntu/project_pol-media-use/scripts/start_watching_cron.py"
