__author__ = 'dmitrii'
import csv
import sys
import os

with open(sys.argv[1], 'r') as csv_file:
    reader = csv.DictReader(csv_file)
    for row in reader:
        with open("splitted_csvs/" + row["Name"] + "_" + sys.argv[1], 'ab') as out_file:
            writer = csv.writer(out_file)
            if os.stat("splitted_csvs/" + row["Name"] + "_" + sys.argv[1]).st_size == 0:
                print row.keys()
                writer.writerow(row.keys())
            writer.writerow(row.values())