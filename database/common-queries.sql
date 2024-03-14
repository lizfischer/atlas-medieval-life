-- Women named in bonds
SELECT p.display_name, d.source, d.source_number FROM person_named_in_document
INNER JOIN documents d on d.document_id = person_named_in_document.document_id
INNER JOIN people p on p.person_id = person_named_in_document.person_id
WHERE d.type="bond" AND p.gender="W"
GROUP BY p.display_name;


-- UPDATE documents SET display_name = source || ' ' || documents.source_number;
UPDATE documents SET display_name = 'RBLR ' || documents.handlist_number WHERE handlist_number not null;
PRAGMA foreign_key_check;



-- Doc Nodes
SELECT document_id as ID, type, source, source_number, handlist_number, display_name as Label, date_text, date_notes,
      d.earliest_date, d.latest_date, "Document" as NodeType
FROM documents
LEFT OUTER JOIN dates d ON documents.date = d.date_id;

-- People Nodes
SELECT person_id as ID, display_name as Label, gender, clerical, "Person" as NodeType
FROM people;



-- People in Docs ALL
SELECT person_id as source, document_id as target, pdr.relationship_id, dead,
       GROUP_CONCAT(DISTINCT person_name_transcription) as person_name_transcription,
       GROUP_CONCAT(DISTINCT named_by) as named_by,
       GROUP_CONCAT(role, '|') as roles, certainty, COUNT(person_id) as weight
From person_named_in_document
LEFT OUTER JOIN person_document_roles pdr on person_named_in_document.relationship_id = pdr.relationship_id
GROUP BY source, target ;


-- People in Docs HCM
SELECT pnd.relationship_id as source, pnd.document_id as target, pnd.person_id, pnd.dead,
       GROUP_CONCAT(DISTINCT person_name_transcription) as person_name_transcription,
       GROUP_CONCAT(DISTINCT pnd.named_by) as named_by,
       GROUP_CONCAT(role, '|') as roles, certainty, COUNT(person_id) as weight
FROM person_named_in_document pnd
LEFT OUTER JOIN person_document_roles pdr on pnd.relationship_id = pdr.relationship_id
INNER JOIN documents d ON pnd.document_id = d.document_id
WHERE d.source = "HCM"
GROUP BY pnd.relationship_id, pnd.document_id;


-- People in Docs RBLR
SELECT pnd.relationship_id, pnd.document_id, pnd.person_id, pnd.dead,
       GROUP_CONCAT(DISTINCT person_name_transcription) as person_name_transcription,
       GROUP_CONCAT(DISTINCT pnd.named_by) as named_by,
       GROUP_CONCAT(role, '|') as roles, certainty, COUNT(person_id) as weight
FROM person_named_in_document pnd
INNER JOIN documents d ON pnd.document_id = d.document_id
LEFT OUTER JOIN person_document_roles pdr on pnd.relationship_id = pdr.relationship_id
WHERE d.display_name LIKE "%RBLR%"
GROUP BY pnd.relationship_id, pnd.document_id;



-- People-People by Shared Docs (all)
SELECT pnd1.person_id as source, pnd2.person_id as target,
       GROUP_CONCAT(d.display_name) as label,
       COUNT(d.document_id) as weight--pnd1.relationship_id, pnd1.document_id, p1.display_name, pnd2.relationship_id, pnd2.document_id, p2.display_name
FROM person_named_in_document pnd1
INNER JOIN documents d ON pnd1.document_id = d.document_id
CROSS JOIN person_named_in_document pnd2 ON pnd1.document_id = pnd2.document_id
WHERE pnd2.person_id != pnd1.person_id
GROUP BY pnd1.person_id, pnd2.person_id;


-- People-People by Shared Docs (HCM)
SELECT pnd1.person_id as source, pnd2.person_id as target,
       GROUP_CONCAT(d.display_name) as label,
       COUNT(d.document_id) as weight--pnd1.relationship_id, pnd1.document_id, p1.display_name, pnd2.relationship_id, pnd2.document_id, p2.display_name
FROM person_named_in_document pnd1
INNER JOIN documents d ON pnd1.document_id = d.document_id
CROSS JOIN person_named_in_document pnd2 ON pnd1.document_id = pnd2.document_id
WHERE pnd2.person_id != pnd1.person_id AND d.source = "HCM"
GROUP BY pnd1.person_id, pnd2.person_id;
