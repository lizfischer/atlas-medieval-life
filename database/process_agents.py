import csv
from tqdm import tqdm

with open("all_people.csv", "r", encoding="utf8") as f:
    people = [{k: v for k, v in row.items()}
         for row in csv.DictReader(f, skipinitialspace=True)]

id_map = {}
for p in people:
    uuids = p['UUID'].split(';')
    for uuid in uuids:
        id_map[uuid.strip()] = p['Person ID']


with open("agents.csv", "r", encoding="utf8") as f:
    agents = [{k: v for k, v in row.items()}
              for row in csv.DictReader(f, skipinitialspace=True)]


errors = []
for a in tqdm(agents):
    if a['relation'] == "Agent":
        try:
            a['source_id_matched'] = id_map[a['source_id']]

        except KeyError:
            a['error'] = 'source id not matched'
            errors.append(a)

        try:
            a['target_id_matched'] = id_map[a['target_id']]
        except KeyError:
            a['error'] = 'target id not matched'
            errors.append(a)

keys = errors[0].keys()
with open('agent_errors.csv', "w", newline='') as output_file:
    dict_writer = csv.DictWriter(output_file, keys)
    dict_writer.writeheader()
    dict_writer.writerows(errors)

