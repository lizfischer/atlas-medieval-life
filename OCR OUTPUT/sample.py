import os, shutil, random

full_pool = os.listdir("ALL DOCUMENTS TXT")  # handlist + hcm + hcm2 + fix
small_sample = os.listdir("GIS Tag Test small")
large_sample = os.listdir("GIS Tag Test large")

already_used = small_sample + large_sample


def random_sample():
    while True:
        new_sample = random.sample(full_pool, 100)
        duplicated = [s for s in new_sample if s in small_sample]
        print(len(duplicated))
        if len(duplicated) == 0:
            break
    print(len(new_sample))

    for f in new_sample:
       shutil.copyfile(os.path.join("ALL DOCUMENTS TXT", f), os.path.join("GIS rest", f))

def get_rest(already_used):
    for f in full_pool:
        if f not in already_used:
            shutil.copyfile(os.path.join("ALL DOCUMENTS TXT", f), os.path.join("GIS rest", f))
            print(f)

import math
def make_batches(files, batch_size):
    n_files = len(files)
    n_batches = math.ceil(n_files / batch_size)
    for i in range(0, n_batches):
        start = i * batch_size
        batch_files = files[start:start+batch_size]
        os.mkdir(f"GIS rest/{i+1}")
        for f in batch_files:
            shutil.move(os.path.join("GIS rest", f), os.path.join(f"GIS rest/{i+1}", f))
        



make_batches(os.listdir("GIS rest"), 10)

def check_numbers():
    ## HCM "UNCORRECTED"
    hcm_dir = os.listdir("hcm-all-uncorrected")
    hcm = []
    for subdir in hcm_dir:
        path = os.path.join("hcm-all-uncorrected", subdir)
        files = os.listdir(path)
        #for f in files:
        #    shutil.copyfile(os.path.join(path, f), os.path.join("ALL DOCUMENTS", f))
        hcm += files


    ## HANDLIST
    handlist_dir = os.listdir("handlist")
    handlist = []
    for subdir in handlist_dir:
        path = os.path.join("handlist", subdir)
        files = os.listdir(path)
        #for f in files:
        #    shutil.copyfile(os.path.join(path, f), os.path.join("ALL DOCUMENTS", f))
        handlist += files

    ## TXT-HCM
    hcm2 = os.listdir("text-hcm")

    ## ADDED TODAY
    fix = os.listdir("embedded docs and bugfix docs")

    full_pool = os.listdir("ALL DOCUMENTS")#handlist + hcm + hcm2 + fix

    print(len(full_pool))

    with open("openrefine_list_of_docs", 'r') as f:
        or_docs = f.readlines()
        or_docs = [t.split("\t")[0] for t in or_docs]

    for doc in full_pool:
        name = doc.replace("_", " ")[:-4] #+".txt"
        if name not in or_docs:
            print("Missing from OpenRefine: ", name)
    for doc in or_docs:
        name = doc.replace(" ", "_")+".txt"
        if name not in full_pool:
            print("Missing from Local Files: ", name)


    import collections
    dupe =  [item for item, count in collections.Counter(full_pool).items() if count > 1]
    for d in dupe: print("Duplicate: ", d)
