__author__ = 'dmitrii'
import csv

param_list = {'app': "app4", 'flac': "cr_audio1.flac", 'wav': "cr_audio1.wav",
              'enw8': "enwik8", 'enw9': "enwik9", 'game': "game1",
              '01': "01",'02': "02",'03': "03",'04': "04",'05': "05",'06': "06",'07': "07",
              '08': "08",'09': "09",'10': "10",'11': "11",'12': "12",'13': "13",'14': "14",
              '16': "16",'17': "17",'18': "18",'19': "19",'20': "20",'21': "21",'22': "22",
              'sort':"sort", 'encrypt':"encrypt", 'decrypt':"decrypt"}
repeat = 7.
energy = {}
time = {}
name = 'results_22'

with open(name + ".csv", 'r') as csv_file:
    reader = csv.DictReader(csv_file)
    for row in reader:
        energy[tuple([row["TR"],row["FR"],row["Name"]])] =0.
        time[tuple([row["TR"], row["FR"],row["Name"]])] =0.

with open(name + ".csv", 'r') as csv_file:
    reader = csv.DictReader(csv_file)
    for row in reader:
        energy[tuple([row["TR"],row["FR"],row["Name"]])] += float(row["EN"])
        time[tuple([row["TR"], row["FR"],row["Name"]])] += float(row["TIM"])
for en in energy.values():
    en /= repeat
for tim in time.values():
    tim /repeat

with open(name +"_avg.csv", 'ab') as output:
    fieldnames = ["FR", "TR", "Name", "EN", "TIM"]
    writer = csv.DictWriter(output, dialect='excel', fieldnames=fieldnames)
    writer.writeheader()
    # print old_row
    for key in energy.keys():
        print str(key[1])
        writer.writerow({'FR': str(key[1]), 'TR': str(key[0]), 'Name': str(key[2]),
                         'EN': str(energy[key]), 'TIM': str(time[key])})
#
# with open('Count_200_mio.csv', 'r') as csv_file:
#     reader = csv.DictReader(csv_file)
#     old_row = None
#     overall_energy = None
#     for row in reader:
#         if not old_row:
#             old_row = row
#             overall_energy = 0.
#             overall_time = 0.
#             continue
#         if row:
#             if row["Name"] == old_row["Name"] and int(row["REP"]) > int(old_row["REP"]):
#                 if int(old_row["REP"]) == 2:
#                     overall_energy += float(old_row["EN"])
#                 overall_energy += float(row["EN"])
#                 overall_time += float(row["TIM"])
#                 old_row = row
#             else:
#                 with open('Count_200_mio_avg.csv', 'ab') as output:
#                     fieldnames = ["FR", "TR", "Name", "EN", "TIM"]
#                     writer = csv.DictWriter(output, dialect='excel', fieldnames= fieldnames)
#                     #print old_row
#                     writer.writerow({'FR':str(float(old_row["FR"])),'TR': str(old_row["TR"]), 'Name': old_row["Name"],'EN': str(overall_energy/7), 'TIM': str(overall_time/7)})
#                 old_row = row
#                 overall_energy = 0.
#                 overall_time = 0.

