import pandas as pd
import json
import os
from os import listdir
from os.path import isfile, join
import multiprocessing as mp

#datadir = os.path.join('C:/', 'data', 'poltweets')
datadir = os.path.join('/home', 'ubuntu', 'data', 'poltweets')
datapath = os.path.join(datadir, 'tweets')
datafiles = [join(datapath,f) for f in listdir(datapath) if isfile(join(datapath, f))]
datafiles = [datafile for datafile in datafiles if datafile.endswith('.ndjson')]

# Parameters
poolsize = 8
outdir = os.path.join(datadir, 'poltweets_combined_20210421.gz')


def read_datafiles(datafiles):
    records_all = list()
    for datafile in datafiles:
        records = map(json.loads, open(datafile, encoding = 'utf-8'))
        records_all = records_all + list(records)
    df = pd.DataFrame.from_records(records_all)
    return(df)

def split_job(datafiles, poolsize = 4):
    combined_df = pd.DataFrame()
    folds = []
    pool = mp.Pool(poolsize)
    split = poolsize
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

def run_and_save(poolsize = 4):
    tweets_df = split_job(datafiles, poolsize = poolsize)
    savepath = outdir
    tweets_df.to_csv(savepath, compression='gzip')

if __name__ == '__main__':
    run_and_save(poolsize = poolsize)
