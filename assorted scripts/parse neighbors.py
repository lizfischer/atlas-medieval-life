import re

from striprtf.striprtf import rtf_to_text
import json
import csv
import pandas


def parse_rtf():
    file = "d:\Desktop\AML\RECOGITO OUTPUT\\Neighbors_Batch_1_to_84.rtf"
    test = "D:\Desktop\AML\\assorted scripts\\test"

    all_groups = []
    current_doc = ""
    current_group = []

    with open(file, "r", encoding='utf-8') as f:
        for line in f:
            txt = rtf_to_text(line).strip().replace("\u2019", "'")

            if not txt: continue  # skip blank lines
            if "Batch" in txt: continue  # skip batch names

            if "HCM" in txt or "RBLR" in txt:  # New document
                if not current_doc:
                    current_doc = txt
                else:
                    all_groups.append({"doc": current_doc, "neighbors": current_group})
                    current_doc = txt
                    current_group = []

            if "no neighbors" in txt: continue  # skip no neighbor lines
            if "are neighbors" in txt:
                # save previous group
                if current_group:
                    all_groups.append({"doc": current_doc, "neighbors": current_group})
                # start new group
                current_group = []
                next = rtf_to_text(f.readline()).strip()
                while next:
                    current_group.append(next)
                    next = rtf_to_text(f.readline()).strip()

    with open("neighbors-grouped.json", "w") as out:
        json.dump(all_groups, out, indent=4)

    return "neighbors-grouped.json"


def search(df, doc_number, keyword):
    search_term = keyword.lower()
    document = df.loc[df["Document Number"] == doc_number.lower()]

    # SEARCH DOCUMENT NORMALIZED TEXT
    normalized = document.loc[document['Normalized text'] == search_term]
    if len(normalized) != 0:
        return normalized["Person ID"].iloc[0]

    # SEARCH DOCUMENT QUOTED TEXT
    quote = document.loc[document['QUOTE_TRANSCRIPTION'] == search_term]
    if len(quote) != 0:
        return quote["Person ID"].iloc[0]

    # SEARCH FOR SUBSTRING IN DOCUMENT QUOTED TEXT
    quote_partial = document.loc[document['QUOTE_TRANSCRIPTION'].str.contains(re.escape(search_term), na=False)]
    if len(quote_partial) != 0:
        return quote_partial["Person ID"].iloc[0]

    # SEARCH DOCUMENT WITHOUT "de" and "of"
    quote_partial = document.loc[document['QUOTE_TRANSCRIPTION'].str.contains(re.escape(search_term.replace(" de ", " ").replace(" of ", " ")), na=False)]
    if len(quote_partial) != 0:
        return quote_partial["Person ID"].iloc[0]

    # SEARCH DOCUMENT NORMALIZED TEXT WITHOUT APOSTROPHE
    search_term = search_term.replace("'", "")
    normalized_notick = document.loc[document['Normalized text'] == search_term]
    if len(normalized_notick) != 0:
        return normalized_notick["Person ID"].iloc[0]

    # SEARCH DOCUMENT QUOTE TEXT WITHOUT APOSTROPHE
    search_term = search_term.replace("'", "")
    quote_notick = document.loc[document['Normalized text'] == search_term]
    if len(quote_notick) != 0:
        return quote_notick["Person ID"].iloc[0]

    # SEE IF DOCUMENT NAMES ARE PARTIALS OF SEARCH NAME
    for index, row in document.iterrows():
        norm = row["Normalized text"]
        quot = row["QUOTE_TRANSCRIPTION"]
        if str(norm) in search_term or str(quot) in search_term:
            print("HALLELUJAH")
            return row["Person ID"]


    # SEE IF THERE'S EXACTLY ONE FIRST NAME MATCH
    search_term = search_term.replace(",","")
    norm_first = document.loc[document['Normalized text'].str.contains(re.escape(search_term.split(" ")[0]), na=False)]
    if len(norm_first) == 1:
        return norm_first["Person ID"].iloc[0]
    quote_first = document.loc[document['Normalized text'].str.contains(re.escape(search_term.split(" ")[0]), na=False)]
    if len(quote_first) == 1:
        return quote_first["Person ID"].iloc[0]


    return "NOT FOUND"


def find_ids(data_file):
    df = pandas.read_csv("All-People.tsv", sep="\t")
    df = df.applymap(lambda s: s.lower() if type(s) == str else s)
    with open(data_file, "r") as f:
        data = json.load(f)

    new_data = []
    for group in data:
        group_with_ids = {}
        for name in group["neighbors"]:
            name = name.split(",")[0]
            doc_number = group["doc"]
            id = search(df, doc_number, name)
            group_with_ids[name] = id
        new_data.append({
            "doc": doc_number,
            "neighbors": group_with_ids
        })

    with open("groups-with-ids-new.json", "w") as out:
        json.dump(new_data, out, indent=4)


find_ids("neighbors-grouped.json")
