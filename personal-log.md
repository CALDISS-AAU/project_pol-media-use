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
- Added "Susan Kronborg" to news collection



#### 2021-09-09

- Added the following Twitter handles to extract:
  - @rvthorholm (Christina Thorholm)
- Added the following names to news collection:
  - Christina Thorholm
  - Anne Rasmussen
- Removed the following Twitter handles from extraction:
  - @Kristian_Jensen 
  - @oestergaard (Morten Østergaard)
  - @aahlers (Tommy Ahlers) 
  - @KHegaard (Kristian Hegaard)
- Removed the following names from news collection:
  - Kristian Jensen 
  - Morten Østergaard
  - Tommy Ahlers
  - Kristian Hegaard



#### 2021-10-08

- Patching fp_watcher to match changes to https://nyheder.tv2.dk/politik 



#### 2022-01-10

- Adding "Gitte Willumsen" to news collection (`modules/mp_checker.py`)
- Removing "Inger Støjberg" from news collection (`modules/mp_checker.py`)



#### 2022-02-03

- Removing "Karsten Lauritzen" from news collection (`modules/mp_checker.py`)
- Removing "Karsten Lauritzen" from tweet collection
- Adding "Maja Torp" to news collection (`modules/mp_checker.py`)
- Adding "Maja Torp" (@MajaTorpAalborg) to tweet collection



#### 2022-02-16

- Downloading missing texts on UCloud using `textdl_20220216.py` (in kgk directory)
  - Using combined set from 2022-02-10
  - Simple download: try with current functions, skip if any errors
  - Set with texts: `articles_combined_2022-02-10_with-texts_20220217.json`
- Encountered changes in URLs for Berlingske - *need manual revision*
- Encountered errors in `mp_matches` - possibly matching other articles on news site - *needs revision*



#### 2022-02-23

- Updating combined set on worker with updated set with texts: `articles_combined_2022-02-23.json`
- 3675 missing texts
- 17870 with text
- Next merge on 2022-02-24 will combine new articles with set with downloaded texts



#### 2022-05-06

- Adding "Maria Gudme" (@mariagudme) to tweet and news collection
- Removing "Nick Hækkerup" from news collection (does not have a twitter profile - never part of tweet collection)
- Updating `polhandles.txt` in repository
  - Converting to lower-case
- Updating cronjob to get polhandles from repository



#### 2022-08-01

- Adding "Susanne Eilersen" (@Eilersen_DF) to tweet and news collection
- Removing "Kristian Thulesen Dahl" (@Kristianthdahl) from tweet and news collection



#### 2022-12-12

- Ending data collection (news and twitter)



#### 2022-12-13

- Trying to retrieve missing texts using `textdl_20221212.py` (under kgk directory)


#### 2022-12-22

- Downloading raw html files using `articledl_20221222.py` in kgk directory - files stored in data/articles
- Downloaded 1974/35873
- Reason for downloading stopped unknown - no links added to list of failed URLs

#### 2023-01-27

- Continue downloading raw html files using `articledl_20221222.py` in kgk directory - files stored in data/articles 
- Starting script on descriptives

#### 2023-02-14

- Continue downloading raw html files using `articledl_20221222.py` in kgk directory - files stored in data/articles 
- Resolved issue caused by UnicodeDecodeError for some links
- Created articles subset (`scripts/articles_subset.py`): `articles_subset_2023-02-14.json`
  - Date filter (after 2020-09-01)
  - Filter links from irrelevant subsections
  - Add filename for raw html


#### 2023-02-20

- Continue downloading raw html files using `articledl_missingfiles_20230220.py` in kgk directory - files stored in data/articles
- Missing files based on article filenames in `articles_subset_2023-02-14.json`