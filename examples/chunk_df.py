def iter_documents(top_directory):
    """
    Generator: iterate over all relevant documents, yielding one
    document (=list of utf8 tokens) at a time.
    """
    col_list = ["created_at", "content"]
    # get current working directory and join with data path
    cwd = os.getcwd()
    datapath = os.path.join(cwd, "data")
    files = sorted(os.listdir(datapath))
    # read data
    for data in files:
        if data.endswith(".gz"):
            path = os.path.join(cwd, "data", data)
            print(f"working on {path}")
            # chunk and process
            for chunk in pd.read_csv(path, chunksize=2000, usecols=col_list):
                #text = list(chunk["content"])
                #meta = list(chunk["created_at"])
                yield chunk