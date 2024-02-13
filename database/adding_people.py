from csv import DictReader
from tqdm import tqdm
import sqlite3

connection = sqlite3.connect('atlas_database_jan_2024.db')
connection.execute("PRAGMA foreign_keys = 1")

cursor = connection.cursor()


def _parse_all_people(input_file):
    with open(input_file, "r", encoding="utf8") as f:
        reader = DictReader(f)
        person_list = list(reader)

    people = []
    for p in person_list:
        people.append(p)
    return people


def _lookup_person(person_info):
    query = '''SELECT * FROM people 
                WHERE person_id = ?'''
    cursor.execute(query, (person_info['Person ID'],))
    result = cursor.fetchall()
    return result


def get_doc_id_by_sourcenum(source: str, num: str) -> list:
    if source.upper() == "RBLR":
        query = '''SELECT document_id FROM documents 
               WHERE handlist_number = ?'''
        cursor.execute(query, (num,))
    else:
        query = '''SELECT * FROM documents 
                   WHERE source = ?
                   AND source_number = ?'''
        cursor.execute(query, (source, num,))
    result = cursor.fetchone()
    if not result:
        raise Exception("Document number not found")
    return result[0]


def _lookup_person_in_doc(person_id, doc_id):
    query = '''SELECT relationship_id FROM person_named_in_document 
                  WHERE person_id = ?
                  AND document_id = ?'''
    cursor.execute(query, (person_id, doc_id,))
    result = cursor.fetchone()
    return result


def _insert_person_in_doc(p, doc_id):
    if _lookup_person_in_doc(p['Person ID'], doc_id):
        return
    query = '''INSERT INTO person_named_in_document(document_id, person_id, person_name_transcription, dead, named_by)
                VALUES(?, ?, ?, ?, ?)'''
    cursor.execute(query, (doc_id, p['Person ID'], p['QUOTE_TRANSCRIPTION'], int(bool(p['Dead'])), p['Named by']))
    connection.commit()


def _lookup_person_role(rel_id, role):
    query = '''SELECT * FROM person_document_roles WHERE relationship_id = ? AND role = ?'''
    cursor.execute(query, (rel_id, role,))
    result = cursor.fetchone()
    return result


def _insert_person_roles(p, doc_id):
    rel_id = _lookup_person_in_doc(p['Person ID'], doc_id)[0]

    query = '''INSERT INTO person_document_roles(relationship_id, role) VALUES (?, ?)'''
    if p['Principal'] and not _lookup_person_role(rel_id, p['Principal']):
        cursor.execute(query, (rel_id, "Principal"))
    if p['Scribe'] and not _lookup_person_role(rel_id, p['Scribe']):
        cursor.execute(query, (rel_id, "Scribe"))
    if p['Witness'] and not _lookup_person_role(rel_id, p['Witness']):
        cursor.execute(query, (rel_id, "Witness"))


def insert_people(input_file="all_people.csv"):
    query = '''INSERT INTO people(person_id, display_name, gender, clerical) VALUES (?,?,?,?)'''
    people = _parse_all_people(input_file)
    for p in tqdm(people):
        if not _lookup_person(p):
            # Add person
            if not p['Gender']:
                p['Gender'] = "U"
            cursor.execute(query, (p['Person ID'], p['Normalized text'], p['Gender'], int(bool(p['Clerical?'])),))

        source, num = p['Doc Number'].split(" ")
        try:
            doc_id = get_doc_id_by_sourcenum(source, num)
            _insert_person_in_doc(p, doc_id)
            _insert_person_roles(p, doc_id)
        except Exception as e:
            with open("errors.txt", "a") as error_file:
                error_file.write(f"Error: {e} on {p}\n")
        connection.commit()


insert_people()
