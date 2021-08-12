import os, math

DIR = 'semester docs/RBLR'
docs = [f for f in os.listdir(DIR) if os.path.isfile(os.path.join(DIR, f))]

BATCH_START = 85
n_batches = math.ceil(len(docs)/10)

for i in range(0, n_batches):
    folder_name = f"Batch {BATCH_START+i}"
    os.mkdir(os.path.join(DIR, folder_name))
    for j in range(0, 10):
        os.rename(f"{DIR}/{docs[i*10+j]}", f"{DIR}/{folder_name}/{docs[i*10+j]}")
