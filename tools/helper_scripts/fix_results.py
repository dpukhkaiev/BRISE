__author__ = 'dmitrii'
import csv

param_list = {'app': "app4", 'flac': "cr_audio1.flac", 'wav': "cr_audio1.wav",
                                          'enw8': "enwik8", 'enw9': "enwik9", 'game': "game1",
                                          '01': "01",'02': "02",'03': "03",'04': "04",'05': "05",'06': "06",'07': "07",
                                          '08': "08",'09': "09",'10': "10",'11': "11",'12': "12",'13': "13",'14': "14",
                                          '16': "16",'17': "17",'18': "18",'19': "19",'20': "20",'21': "21",'22': "22", 'sort':"sort"}

with open('results.csv', 'r') as csv_file:
    reader = csv.DictReader(csv_file)
    old_row = None
    overall_energy = None
    for row in reader:
        if not old_row:
            old_row = row
            overall_energy = 0.
            overall_time = 0.
            continue
        if row:
            if row["Name"] == old_row["Name"] and int(row["REP"]) > int(old_row["REP"]):
                if int(old_row["REP"]) == 2:
                    overall_energy += float(old_row["EN"])
                overall_energy += float(row["EN"])
                overall_time += float(row["TIM"])
                old_row = row
            else:
                with open('results_avg.csv', 'ab') as output:
                    fieldnames = ["FR", "TR", "Name", "EN", "TIM"]
                    writer = csv.DictWriter(output, dialect='excel', fieldnames= fieldnames)
                    #print old_row
                    writer.writerow({'FR':str(float(old_row["FR"])),'TR': str(old_row["TR"]), 'Name': old_row["Name"],'EN': str(overall_energy/7), 'TIM': str(overall_time/7)})
                old_row = row
                overall_energy = 0.
                overall_time = 0.

    with open('results_avg.csv', 'ab') as output:
        fieldnames = ["FR", "TR", "Name", "EN", "TIM"]
        writer = csv.DictWriter(output, dialect='excel', fieldnames= fieldnames)
        #print old_row
        writer.writerow({'FR':str(float(old_row["FR"])),'TR': str(old_row["TR"]), 'Name': old_row["Name"],'EN': str(overall_energy/7), 'TIM': str(overall_time/7)})