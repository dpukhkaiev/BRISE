__author__ = 'dmitrii'
import csv
from os import walk

freqs = [1200.0,1300.0, 1400.0, 1600.0, 1700.0, 1800.0, 1900.0, 2000.0, 2200.0, 2300.0, 2400.0, 2500.0, 2700.0, 2800.0, 2900.0, 2901.0]
threads = [1, 2, 4, 8, 16, 32]
energy ={}
time={}
subset_energy={}
subset_time={}
#max_deviation={}
repeats = 10.

for f in freqs:
    for t in threads:
        energy[tuple([str(f),str(t)])] = 0.
        time[tuple([str(f),str(t)])] = 0.
        subset_energy[tuple([str(f),str(t)])] = 0.
        subset_time[tuple([str(f),str(t)])] = 0.
        #max_deviation[tuple([str(f),str(t)])] = 0


for dirpath,dirnames,filenames in walk("../doc/thesis/measurements/final_near_optimal/full_sort/"):
    for file in filenames:
        with open("../doc/thesis/measurements/final_near_optimal/full_sort/"+file, 'r') as csv_file:
            reader = csv.DictReader(csv_file)
            #print csv_file
            for row in reader:

                f = row["FR"]
                t = row["TR"]

                energy[tuple([f,t])]+=float(row["EN"])
                time[tuple([f,t])]+=float(row["TIM"])

# for dirpath,dirnames,filenames in walk("../doc/thesis/measurements/final_near_optimal/subsets_compress/"):
# ../doc/thesis/measurements/final_near_optimal/subset_encrypt/
for dirpath, dirnames, filenames in walk("../../../../../work/st/fase17-brise/measurements/fedorov/subsets/subsets_sort/"):

    print filenames
    for file in filenames:
        # with open("../doc/thesis/measurements/final_near_optimal/subsets_compress/"+file, 'r') as csv_file:
        with open("../../../../../work/st/fase17-brise/measurements/fedorov/subsets/subsets_sort/"+file, 'r') as csv_file:
            #print csv_file
            reader = csv.DictReader(csv_file)
            for row in reader:
                f = row["FR"]
                t = row["TR"]
                # print csv_file
                subset_energy[tuple([f,t])]+=float(row["EN"])
                subset_time[tuple([f,t])]+=float(row["TIM"])

# with open('../hill_climber_10.csv', 'r') as csv_file:
#     reader = csv.DictReader(csv_file)
#     overall_energy = 0.
#     overall_time = 0.
#
#     for row in reader:
#         if row["REP"] == str(1):
#             overall_energy += float(row["OV_EN"])
#             overall_time += float(row["OV_TIM"])




print "OE " + str(sum(energy.values()))
print "OR " + str(sum(subset_energy.values()))
# print "OHC " + str(overall_energy)
print 1 - sum(subset_energy.values())/sum(energy.values())
# print 1 - overall_energy/sum(energy.values())



print "\nOT " + str(sum(time.values())/60/60/24)
print "ORT " + str(sum(subset_time.values())/60/60/24)
# print "OHCT " + str(overall_time/60/60/24)
print 1 - sum(subset_time.values())/sum(time.values())
# print 1 - overall_time/sum(time.values())

ffd_en = {}
ffd_time = {}

# threads_all = [i for i in range(1,33,1)]
# for f in freqs:
#     for t in threads_all:
#         ffd_en[tuple([str(f),str(t)])] = 0.
#         ffd_time[tuple([str(f),str(t)])] = 0.

# for dirpath,dirnames,filenames in walk("../csvs/"):
#     for file in "pigz_compress_full_avg.csv":
#         with open("../csvs/pigz_compress_full_avg.csv", 'r') as csv_file:
#             reader = csv.DictReader(csv_file)
#             #print csv_file
#             for row in reader:
#
#                 f = row["FR"]
#                 t = row["TR"]
#                 ffd_en[tuple([f,t])]+=float(row["EN"])
#                 ffd_time[tuple([f,t])]+=float(row["TIM"])
#
# print "\nFULLLLLLEEEE " + str(sum(ffd_en.values()))
# print "\nFULLLLLLTTTT " + str(sum(ffd_time.values())/60/60)
# print len(ffd_en)