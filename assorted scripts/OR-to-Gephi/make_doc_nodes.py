import pandas as pd


doc_df = pd.read_csv('../../document processing/OPEN REFINE/Document-Info.csv')

output_df = pd.DataFrame({
    "ID": doc_df['Document Number'],
    "Label": doc_df['Alternate Numbering'],
    "Date (earliest)": doc_df['Earliest Date'],
    "Date (latest)": doc_df['Latest Date'],
    "Doc Type": doc_df['Doc Type'],
    "Given At": doc_df['Given At'],
    "Given At Certainty": doc_df['Given At Certainty']
})
output_df.to_csv('../../Gephi/inputs/nodes_documents.csv', index=False)

