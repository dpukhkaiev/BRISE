__author__ = 'dmitrii'
import csv
import sys
from os import walk

freqs = [1200.0,1300.0, 1400.0, 1600.0, 1700.0, 1800.0, 1900.0, 2000.0, 2200.0, 2300.0, 2400.0, 2500.0, 2700.0, 2800.0, 2900.0, 2901.0]

threads = [1, 2, 4, 8, 16, 32]
energy ={}
to_add={}
#max_deviation={}
repeats = 7.
header = ['FR', 'EN', 'END', 'Name', 'START', 'REP', 'TR', 'TIM']
for f in freqs:
    for t in threads:
        energy[tuple([str(f),str(t)])] = 0.
        to_add[tuple([str(f),str(t)])] = 0
        #max_deviation[tuple([str(f),str(t)])] = 0


#for dirpath,dirnames,filenames in walk("../doc/thesis/measurements/final_near_optimal/subsets_encrypt/"):

with open(sys.argv[1], 'r') as csv_file:
    reader = csv.DictReader(csv_file)
    for row in reader:
        f = row["FR"]
        t = row["TR"]


        energy[tuple([f,t])]+=float(row["EN"])
#print energy

for config in energy.keys():
    if energy[config] > 0.:
        to_add[config] = 1

#print to_add
for config in to_add.keys():
    if to_add[config]==1:
        with open(sys.argv[2], 'r') as csv_file:
            reader = csv.DictReader(csv_file)
            for row in reader:
                f = row["FR"]
                t = row["TR"]
                rep = row["REP"]
                if tuple([f,t]) == config and int(rep) == 1 and sys.argv[3]==row["Name"]:
                    with open(sys.argv[1], 'ab') as csv_file2:
                        writer = csv.DictWriter(csv_file2,header)
                        writer.writerow(row)
