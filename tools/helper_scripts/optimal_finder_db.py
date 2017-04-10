__author__ = 'dmitrii'

import csv
import sys

file_name = sys.argv[1][:-4]

with open(file_name + ".csv", 'r') as csv_file:
    reader = csv.DictReader(csv_file)
    old_row = None
    min_energy = None
    settings = {}

    for row in reader:
        if row["REP"] == "1":
            if not old_row:
                old_row = row
                min_energy = 0.
                settings[tuple([row["DataType"],row["ACT"]])] = row
                continue


            if settings.has_key(tuple([row["DataType"],row["ACT"]])):
                if float(settings[tuple([row["DataType"],row["ACT"]])]["EN"]) > float(row["EN"]):
                    settings[tuple([row["DataType"],row["ACT"]])] = row
            else:
                settings[tuple([row["DataType"],row["ACT"]])] = row
        #print settings.items()[0][0]
        #exit(0)
    with open(file_name + '_near_optimal.csv', 'ab') as output:
        fieldnames = settings[settings.items()[0][0]].keys()
        writer = csv.DictWriter(output, dialect='excel', fieldnames= fieldnames)
        writer.writeheader()
        # overall_savings = 0.
        # overall_time = 0.
        for s in settings.values():
            writer.writerow(s)
        #     overall_savings += float(s["EN_S"])
        #     overall_time += float(s["TIM_S"])
        #
        # print overall_savings/21
        # print overall_time/21
