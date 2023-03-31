import pandas as pd

people_df = pd.read_csv('../../document processing/OPEN REFINE/All-People.csv')
rel_df = pd.read_csv('../../document processing/OPEN REFINE/All-Relationships.csv')
rel_df = rel_df[rel_df['source_id'].notna()]


def translate_ids(row, field):
    match = people_df.loc[people_df['UUID'].str.contains(row[field], na=False), "Person ID"]
    return None if len(match) == 0 else match.iloc[0]


rel_df['source_person_id'] = rel_df.apply(lambda row: translate_ids(row, 'source_id'), axis=1)
rel_df['target_person_id'] = rel_df.apply(lambda row: translate_ids(row, 'target_id'), axis=1)
rel_df.to_csv("All-Relationships_adjusted-ids.csv")
