__author__ = 'dmitrii'

import csv
filename = 'sim_annealing_results/sim_annealing_compress_01'
with open(filename+'.csv', 'r') as csv_file:
    reader = csv.DictReader(csv_file)
    old_row = None
    min_energy = None
    settings = {}

    for row in reader:
        #if row["REP"] == "3":
        # if row["DataType"] == "cr_audio1.flac" and row["ACT"] == "decompress":
        #     continue
        if not old_row:
            old_row = row
            min_energy = 0.
            settings[tuple([row["Name"],row["ACT"]])] = row
            continue


        if settings.has_key(tuple([row["DataType"],row["ACT"]])):
            if float(settings[tuple([row["DataType"],row["ACT"]])]["EN"]) > float(row["EN"]):
                settings[tuple([row["DataType"],row["ACT"]])] = row
        else:
            settings[tuple([row["DataType"],row["ACT"]])] = row
        #print settings.items()[0][0]
        #exit(0)
    with open(filename+'_out.csv', 'ab') as output:
        fieldnames = settings[settings.items()[0][0]].keys()
        writer = csv.DictWriter(output, dialect='excel', fieldnames= fieldnames)
        writer.writeheader()
        overall_savings = 0.
        overall_time = 0.
        for s in settings.values():
            writer.writerow(s)
            overall_savings += float(s["EN_S"])
            overall_time += float(s["TIM_S"])

        print overall_savings/11.
        print overall_time/11.
