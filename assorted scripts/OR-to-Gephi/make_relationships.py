import pandas as pd
from itertools import combinations
import csv


# PEOPLE THAT SHARE THE SAME DOCUMENT
def people_in_docs(df, filename):
    doc_groups = df.groupby('Document Number')
    with open(filename, 'w') as outfile:
        writer = csv.writer(outfile, lineterminator='\n')
        writer.writerow(['source', 'target', 'label', 'type'])
        for doc_name, group in doc_groups:
            pairs = list(combinations(group['Person ID'], 2))
            for pair in pairs:
                writer.writerow([pair[0], pair[1], doc_name,'Undirected'])




people_df = pd.read_csv('../../document processing/OPEN REFINE/All-People.csv')
doc_df = pd.read_csv('../../document processing/OPEN REFINE/Document-Info.csv')

# HCM ONLY
hcm_only = people_df[people_df['Document Number'].str.contains('HCM')]

people_in_docs(people_df, 'same_doc_relationships_all.csv')
people_in_docs(hcm_only, 'same_doc_relationships_hcm.csv')

