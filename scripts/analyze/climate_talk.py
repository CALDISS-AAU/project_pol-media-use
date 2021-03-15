import pandas as pd
import json
import os
from os import listdir
from os.path import isfile, join
import ast
import numpy as np
import stanza
import re
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
import nltk
from nltk.corpus import stopwords

import matplotlib.pyplot as plt
import seaborn as sns

stanza.download('da')
nltk.download('stopwords')

import_cols = ['created_at', 'id', 'full_text', 'entities', 'user', 'retweeted_status', 'is_quote_status', 'retweet_count', 
            'favorite_count', 'favorited', 'retweeted']

user_infos = ['id', 'name', 'screen_name', 'location', 'description', 'url', 'followers_count', 'created_at', 'verified']

keep_cols = ['created_at', 'id', 'full_text', 'is_quote_status', 'retweet_count', 'favorite_count', 'favorited', 'retweeted',
            'is_retweet', 'hashtags', 'user_mentions', 'urls'] + ["user_" + user_info for user_info in user_infos]

datapath = os.path.join('C:/', 'data', 'poltweets', "tweets_flattened_20200127.gz")
matpath = os.path.join('..','..', 'material')

nlp = stanza.Pipeline('da', processors = 'tokenize,pos') # no sentiment analysis for Danish

# Stopwords
custom_stopwords = ['mere', 'flere']
stopWords = set(stopwords.words('danish') + custom_stopwords)

# Load data
data = pd.read_csv(datapath, index_col = 0)

# Politicians
polparty = pd.read_csv(os.path.join(matpath, 'politicians_party.csv'))
poldict = polparty.groupby('navn')['parti'].apply(list).to_dict()

# Functions
def get_party(user):
    """
    Find political party based on fuzzy string matching on name.
    """
    similarity = 0

    for k,v in poldict.items():
        newsim = fuzz.ratio(user, k)
        if newsim > similarity:
            similarity = newsim
            party = v[0]
    return(party)

def tokenizer_custom(text):
    """
    Tokenizer function.
    """
    doc = nlp(text.lower())
    
    tag_match = re.compile(r'(?!^\@|^\#)')
    
    pos_tags = ['NOUN'] # Keep adjectives and nouns
    
    tokens = []
      
    for sentence in doc.sentences:
        for word in sentence.words:
            if (word.pos in pos_tags) & (word.text not in stopWords):
                token = word.text # Returning the lemma of the word in lower-case.
                tokens.append(token)
    
    tokens = list(filter(tag_match.match, tokens))
    
    return(tokens)

def climate_match(string):
    regex = re.compile(r'.*klima.*|.*miljø.*', re.IGNORECASE)
    
    if regex.match(string):
        return True
    else:
        return False
    
# Adding party variable
users = list(data['user_name'].unique())

userparty = pd.DataFrame({'username': pd.Series(users), 'party': pd.Series(users).apply(get_party)})
userparty_dict = dict(zip(userparty['username'], userparty['party']))

data['party'] = data['user_name'].copy().replace(userparty_dict)

# Format date variable and sort
data['created_at'] = pd.to_datetime(data['created_at'], format = "%a %b %d %H:%M:%S %z %Y")
data = data.sort_values('created_at')

# Adding year_month variable
data['year_month'] = data['created_at'].dt.to_period('M')

# Subsetting: No retweets and only after 2015
df = data.loc[(data['is_retweet'] == False) & (data['created_at'].dt.year >= 2015),:]

# Tweets over time
df_grouped = df.groupby(pd.PeriodIndex(df['created_at'], freq='D'))
results = df_grouped.size().to_frame(name = 'count')
idx = pd.period_range(min(results.index), max(results.index))
results = results.reindex(idx, fill_value = 0)
results['year_week'] = results.index.to_timestamp()
results['year_week'] = results['year_week'].dt.year.astype(str) + "-" + results['year_week'].dt.isocalendar().week.astype(str).str.pad(width = 2, fillchar = '0')

week_counts = results.groupby('year_week')['count'].sum().to_frame(name = 'count').reset_index()