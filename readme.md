# project_pol-media-use



This repository contains software used for collection and handling of Danish news media data for the PhD dissertation [In the crossfield between traditional and social media: A  mixed-methods study of Danish parliamentarians' communication in a  hybrid media environment](https://vbn.aau.dk/en/projects/in-the-crossfield-between-traditional-and-social-media-a-mixed-me).

Please note that this repository is not in active development and is not configured to be able to run as its own module. This repository serves as documentation for how relevant Danish news media data was collected and handled for the project.

All web scraping of Danish news media outlets has been conducted with written consent from the relevant parties. We do not condone using software contained in this repository for scraping said news media outlets without their express consent.



## Contents

This repository primarily contains python modules and scripts used for scraping news articles from the policy section of the following Danish news media outlets:

- DR Nyheder
- TV 2 Nyheder
- Berlingske
- Jyllands-Posten
- Ekstra Bladet
- Politiken

Twitter data on Danish members of parliament was collected using the now defunct Twitter API v2 with academic access. Scripts used for ongoing data appending and handling are also included in this repository.

**Folder structure**

```
├───cron
├───docs
├───envs
├───modules
│   └───deprecated
├───notebooks
│   ├───analyze
│   ├───examples
│   ├───scraper_develop
│   └───twitter_testing
├───scripts
│   ├───analyze
│   ├───datahandling
│   ├───deprecated
│   ├───logs
│   └───scraper
├───scripts_bash
└───workshop
    └───img
```

- `cron`: example of how [`crontab`](https://pubs.opengroup.org/onlinepubs/9699919799/utilities/crontab.html) was set up to periodically run jobs
- `docs`: relevant documentation including description of final data set, relevant changes made to data collection etc.
- `envs`: conda environment YAML files
- `modules`: collection of python modules used in web scraping and data handling
- `notebooks`: collection of various python Jupyter notebooks used throughout the project
- `scripts`: python scripts used for web scraping and data handling
- `scripts_bash`: bash scripts used to run web scraper and data handling jobs
- `workshop`: notebooks used for workshop on web scraping with project participants



**Main files used for data collection and handling**

- `modules/fp_watcher.py`: main python module for scraping news articles
- `modules/textdl.py`: python module for parsing text contents of news articles
- `modules/mp_checker.py`: python module for checking whether Danish member of parliament was mentioned in article
- `modules/mp_checker2.py`: python module for checking whether Danish member of parliament was mentioned in article and whether they were member of parliament at the time the article was published (used as part of final filtering of data)
- `scripts/scraper/start_watching_cron.py`: python script used for running web scraper
- `scripts/scraper/article_text-download.py`: python script used for retrieving missing article texts
- `scripts/datahandling/articles_combine_json_csv.py`: python script used for appending news article data
- `scripts/datahandling/articles_subset.py`: python script used for final subsetting and filtering of news articles data