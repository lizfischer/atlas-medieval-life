import pandas as pd
from itertools import combinations
import csv

people_df = pd.read_csv('All-People.csv')
doc_df = pd.read_csv('Document-Info.csv')

# HCM ONLY
hcm_only = people_df[people_df['Document Number'].str.contains('HCM')]


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


people_in_docs(people_df, 'same_doc_relationships_all.csv')
people_in_docs(hcm_only, 'same_doc_relationships_hcm.csv')

# ALL-PEOPLE TO NODES TABLE
unique_people = people_df.rename(columns={'Person ID': 'ID', 'Normalized text': 'Label'})

agg_methods = {'QUOTE_TRANSCRIPTION': lambda x:';'.join(x),
               'Gender': pd.Series.mode,
               'Label': pd.Series.mode}

unique_people = unique_people.fillna('').groupby('ID').agg(agg_methods)
unique_people = unique_people[['Label', 'Gender', 'QUOTE_TRANSCRIPTION']]
unique_people.to_csv('people_nodes.csv', index=True)
