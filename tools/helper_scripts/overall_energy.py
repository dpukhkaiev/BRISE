__author__ = 'dmitrii'

import csv
nffd_energy = 115.
#374270000
#nffd_time = 38.37
overall_energy = 0.
overall_time = 0.
with open('../hill_climber_1', 'r') as csv_file:
    reader = csv.DictReader(csv_file)
    for row in reader:
        overall_energy += float(row["SUB"])
        #overall_time += float(row["OV_TIM"])/60/60/24

with open('../hill_climber_1_2', 'r') as csv_file:
    reader = csv.DictReader(csv_file)

    for row in reader:
        overall_energy += float(row["SUB"])
        #overall_time += float(row["OV_TIM"])/60/60/24/1000
print overall_energy/nffd_energy-1
#print overall_time/nffd_time-1

