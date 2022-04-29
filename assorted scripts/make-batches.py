import functools
import os, math, pathlib


def prefix_sort(x, y, sep="_", to_int=True):
    x = pathlib.Path(x).stem.split(sep)[1]
    y = pathlib.Path(y).stem.split(sep)[1]
    if to_int:
        x = int(x)
        y = int(y)
    return x - y


DIR = 'd:\Desktop\AML\OCR OUTPUT\BR_Swinfield'
docs = [f for f in os.listdir(DIR) if os.path.isfile(os.path.join(DIR, f))]

docs = sorted(docs, key=functools.cmp_to_key(prefix_sort))

BATCH_START = 1
BATCH_SIZE = 15
n_batches = math.ceil(len(docs)/BATCH_SIZE)

for i in range(0, n_batches):
    folder_name = f"Batch {BATCH_START+i}"
    os.mkdir(os.path.join(DIR, folder_name))
    for j in range(0, BATCH_SIZE):
        os.rename(f"{DIR}/{docs[i*BATCH_SIZE+j]}", f"{DIR}/{folder_name}/{docs[i*BATCH_SIZE+j]}")
