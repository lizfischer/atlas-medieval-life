import pandas as pd

people_df = pd.read_csv('../../document processing/OPEN REFINE/All-People.csv')
unique_people = people_df.rename(columns={'Person ID': 'ID', 'Normalized text': 'Label'})


agg_methods = {'QUOTE_TRANSCRIPTION': lambda x:';'.join(x),
               'Gender': pd.Series.mode,
               'Label': pd.Series.mode}

unique_people = unique_people.fillna('').groupby('ID').agg(agg_methods)
unique_people = unique_people[['Label', 'Gender', 'QUOTE_TRANSCRIPTION']]
unique_people.to_csv('../../Gephi/inputs/nodes_people.csv', index=False)
