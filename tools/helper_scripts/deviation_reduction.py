__author__ = 'dmitrii'
import csv

freqs = [1200.0,1300.0, 1400.0, 1600.0, 1700.0, 1800.0, 1900.0, 2000.0, 2200.0, 2300.0, 2400.0, 2500.0, 2700.0, 2800.0, 2900.0, 2901.0]
threads = [1, 2, 4, 8, 16, 32]
energy ={}
time={}
max_deviation={}
repeats = 10.

for f in freqs:
    for t in threads:
        energy[tuple([str(f),str(t)])] = 0
        time[tuple([str(f),str(t)])] = 0
        max_deviation[tuple([str(f),str(t)])] = 0


for file in ["enwik4-Whirlpool.csv"]:
    with open("../doc/thesis/measurements/final_near_optimal/full_encrypt/"+file, 'r') as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            f = row["FR"]
            t = row["TR"]

            energy[tuple([f,t])]+=float(row["EN"])
            time[tuple([f,t])]+=float(row["TIM"])


to_delete=[]
for file in ["enwik4-Whirlpool.csv"]:
    for config in energy.keys():
        with open("../doc/thesis/measurements/final_near_optimal/full_encrypt/"+file, 'r') as csv_file:
            reader = csv.DictReader(csv_file)


            for row in reader:
                if tuple([row["FR"],row["TR"]]) == config:
                    if abs(float(row["EN"]) - energy[config]/repeats) > max_deviation[config]:
                        if max_deviation[config] > 0:
                            to_delete.pop()
                            to_delete.append(row)
                            max_deviation[config] = abs(float(row["EN"]) - energy[config]/repeats)
                        else:

                            to_delete.append(row)
                            max_deviation[config] = abs(float(row["EN"]) - energy[config]/repeats)

header =  to_delete[0].keys()
for file in ["enwik4-Whirlpool"]:
    with open("../doc/thesis/measurements/final_near_optimal/full_encrypt/"+file+".csv", 'r') as csv_file:
        with open("../doc/thesis/measurements/final_near_optimal/full_encrypt/"+file+"_new.csv", 'ab') as csv_file2:
            reader = csv.DictReader(csv_file)
            writer = csv.DictWriter(csv_file2,header)
            writer.writeheader()
            for row in reader:
                if not to_delete.__contains__(row):
                    writer.writerow(row)
