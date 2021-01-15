import pandas as pd
import json
import os
from os import listdir
from os.path import isfile, join
import multiprocessing as mp

datapath = os.path.join('C:/', 'data', 'poltweets', 'tweets')
datafiles = [join(datapath,f) for f in listdir(datapath) if isfile(join(datapath, f))]
datafiles = [datafile for datafile in datafiles if datafile.endswith('.ndjson')]

def read_datafiles(datafiles):
    df = pd.DataFrame()
    for datafile in datafiles:
        records = map(json.loads, open(datafile, encoding = 'utf-8'))
        df = df.append(pd.DataFrame.from_records(records), ignore_index = True)
    return(df)

def split_job(datafiles):
    combined_df = pd.DataFrame()
    folds = []
    pool = mp.Pool(4)
    split = 4
    length = int(len(datafiles)/split) #length of each fold
    for i in range(split-1):
        folds.append(datafiles[i*length:(i+1)*length])
    folds.append(datafiles[(split-1)*length:len(datafiles)])

    results = []
    for fold in folds:
        results.append(pool.apply_async(read_datafiles, args = (fold, )))

    dfs = [result.get() for result in results]
    for df in dfs:
        combined_df = combined_df.append(df, ignore_index = True)

    return(combined_df)

def run_and_save():
    tweets_df = split_job(datafiles)
    savepath = os.path.join('C:/', 'data', 'poltweets', "tweets_combined_20200115.gz")
    tweets_df.to_csv(savepath, compression='gzip')

if __name__ == '__main__':
    run_and_save()