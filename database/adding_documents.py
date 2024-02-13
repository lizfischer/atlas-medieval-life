from csv import DictReader
from sqlite3 import Connection

from tqdm import tqdm
import sqlite3

connection = sqlite3.connect('atlas_database_jan_2024.db')
connection.execute("PRAGMA foreign_keys = 1")

cursor = connection.cursor()

# cursor.execute('''INSERT INTO documents (type, source, source_number) VALUES ("account", "HCM", "2368")''')
# connection.commit()
# connection.close()


def parse_doc_info(input_file="doc_info.csv"):
    with open(input_file, "r", encoding="utf8") as f:
        reader = DictReader(f)
        doc_list = list(reader)
    docs = []

    for d in doc_list:
        d['Earliest Date'] = d['Earliest Date'].split('T')[0].strip()
        d['Latest Date'] = d['Latest Date'].split('T')[0].strip()
        d['type'] = d['General Doc Type'].strip().lower()
        if "HCM" in d['Alternate Numbering']:
            d['source_num'] = d['Alternate Numbering'].split('HCM ')[1]
            d['source'] = "HCM"
        else:
            d['source'] = None
            d['source_num'] = None
        if "RBLR" in d['Number']:
            d['rblr'] = d['Number'].split(" ")[1]
        else:
            d['rblr'] = None
        docs.append(d)
    return docs


def insert_date(doc_info, commit=False):
    query = '''INSERT INTO dates(earliest_date, latest_date) VALUES(?, ?)'''
    cursor.execute(query, (doc_info['Earliest Date'], doc_info['Latest Date'],))
    if commit:
        connection.commit()
    return cursor.lastrowid


def lookup_date(doc_info):
    query = '''SELECT * FROM dates 
            WHERE earliest_date = ?
            AND latest_date = ?'''

    cursor.execute(query, (doc_info['Earliest Date'], doc_info['Latest Date'],))
    result = cursor.fetchall()
    return result


def _lookup_doc(doc_info):
    query = '''SELECT * FROM documents 
            WHERE source = ?
            AND source_number = ?
            AND handlist_number = ?'''

    cursor.execute(query, (doc_info['source'], doc_info['source_num'], doc_info['rblr'],))
    result = cursor.fetchall()
    return result


def insert_docs(input_file="doc_info.csv"):
    query = '''INSERT INTO documents(type, source, source_number, handlist_number, date, date_text, date_notes) 
                VALUES (?, ?, ?, ?, ?, ?, ?)'''

    docs = parse_doc_info()
    for d in tqdm(docs):
        if _lookup_doc(d):
            continue
        # cursor.execute("INSERT INTO documents(type, source, source_number, handlist_number", ())
        date = lookup_date(d)
        if not date:
            date_id = insert_date(d)
        else:
            date_id = date[0][0]

        cursor.execute(query, (d['type'], d['source'], d['source_num'], d['rblr'], date_id, d['DATE'], d['Date notes'],))
        connection.commit()


def parse_doc_types(input_file="doc_types.csv"):
    with open(input_file, "r") as f:
        lines = f.readlines()
    types = []
    for t in lines:
        types.append(t.strip().lower())

    return types


def insert_doc_types(input_file="doc_types.csv"):
    types = parse_doc_types(input_file)
    for t in types:
        print(t)
        cursor.execute("INSERT INTO document_types (doc_type) VALUES (?)", (t,))
    connection.commit()


connection.close()
