import os
import csv


ENT_FOLDER = "d:\Desktop\AML\RECOGITO OUTPUT\hcm entity csvs"
REL_FOLDER = "d:\Desktop\AML\RECOGITO OUTPUT\hcm relationship csvs"
ENT_MERGED_OUT = "d:\Desktop\AML\RECOGITO OUTPUT\hcm_entities_all.csv "
REL_MERGED_OUT = "d:\Desktop\AML\RECOGITO OUTPUT\hcm_relationships_all.csv"


def merge_files(DIR, OUT):
    first_file = True
    with open(OUT, "w", newline='') as fout:
        writer = csv.writer(fout, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

        for file in os.listdir(DIR):
            with open(os.path.join(DIR, file), "r", newline='') as fin:
                reader = csv.reader(fin)
                if first_file:
                    writer.writerow(next(reader))
                    first_file = False
                    print("Headers")
                for row in reader:
                    print(row)
                    writer.writerow(row)


merge_files(REL_FOLDER, REL_MERGED_OUT)
