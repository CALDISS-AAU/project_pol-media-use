# BP: PolMedUse - Personal log



#### 2021-07-13

- Updated `fp_watcher.py` to use function `mp_checker` from module
- Re-created combined data from 2021-04-21
- Created script `articles_combine_json_csv.py`
  - Reads in existing combined articles file (json)
  - Reads in latest article files (copied via `article_zip-copy.sh`)
  - Filters latest articles based on encounter datetime in existing articles
  - Combines articles
  - Outputs both as JSON and CSV
- Created `articles_zip-copy.sh`
  - Bash job to zip article files from headline watcher and copy them over to worker instance
- Created `articles_combine.sh`
  - Bash job to update data using zipped file of latest articles and `articles_combine_json_csv.py`
- Set up crontab to run `articles_zip-copy.sh` and `articles_combine.sh` every Thursday at 3 AM  and 4 AM respectively



#### 2021-08-09

- Added @kronborgsusan to list of Twitter handles to extract
