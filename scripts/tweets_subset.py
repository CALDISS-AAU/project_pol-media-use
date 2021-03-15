import pandas as pd
import os
from fuzzywuzzy import fuzz
from fuzzywuzzy import process

data_path = os.path.join("D:/", "data", "poltweets")
matpath = os.path.join('..', 'material')
filename = "tweets_flattened_20200127.gz"

tweets_df = pd.read_csv(os.path.join(data_path, filename))

tweets_sample = tweets_df.sample(n = 1000)

outname = "tweets_flattened_sample_20210305.csv"

tweets_sample.to_csv(os.path.join(data_path, outname), index = False)

# Sample party - no user info

# Load data
data = pd.read_csv(os.path.join(data_path, filename), index_col = 0)

# Politicians
polparty = pd.read_csv(os.path.join(matpath, 'politicians_party.csv'))
poldict = polparty.groupby('navn')['parti'].apply(list).to_dict()

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

# Adding party variable

users = list(data['user_name'].unique())

userparty = pd.DataFrame({'username': pd.Series(users), 'party': pd.Series(users).apply(get_party)})
userparty_dict = dict(zip(userparty['username'], userparty['party']))

data['party'] = data['user_name'].copy().replace(userparty_dict)
data['created_at'] = pd.to_datetime(data['created_at'], format = "%a %b %d %H:%M:%S %z %Y")

df = data.loc[(data['is_retweet'] == False) & (data['created_at'].dt.year >= 2015),:]

greenlandp = ['Inuit Ataqatigiit', 'Siumut']

col_keep = ['created_at', 'id', 'full_text', 'is_quote_status', 'retweet_count',
       'favorite_count', 'favorited', 'retweeted', 'is_retweet', 'hashtags',
       'urls', 'user_followers_count', 'party']

tweets_sample = df.loc[~df['party'].isin(greenlandp),col_keep].groupby('party').sample(500)

filename = 'poltweets_sample.csv'
tweets_sample.to_csv(os.path.join(data_path, filename), index = False)