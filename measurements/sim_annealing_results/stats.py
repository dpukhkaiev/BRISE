import csv
from os import walk

number_of_experiments = 5.

overall_savings = 0.
overall_time_savings = 0.
overall_reduced_energy = 0.
overall_reduced_time = 0.
overall_full_energy = 0.
overall_full_time = 0.

with open('sim_annealing_sort_05_near_optimal.csv', 'r') as output:
    reader = csv.DictReader(output)
    for row in reader:
        overall_savings += float(row["EN_S"])
        overall_time_savings += float(row["TIM_S"])



with open('sim_annealing_sort_05.csv', 'r') as output:
    reader = csv.DictReader(output)
    for row in reader:
        overall_reduced_energy += float(row["OV_EN"])
        overall_reduced_time += float(row["OV_TIM"])

for dirpath,dirnames,filenames in walk("../doc/thesis/measurements/final_near_optimal/full_sort/"):
    # print filenames
    for f in filenames:
        with open("../doc/thesis/measurements/final_near_optimal/full_sort/"+f, 'r') as csv_file:
            reader = csv.DictReader(csv_file)
            print f
            for row in reader:

                overall_full_energy+=float(row["EN"])
                overall_full_time+=float(row["TIM"])

print "Energy savings " + str(overall_savings / number_of_experiments)
print "Time savings" + str(overall_time_savings / number_of_experiments)



print "OE " + str(overall_full_energy)
print "OR " + str(overall_reduced_energy)
print 1 - overall_reduced_energy/overall_full_energy/10

print "\nOT " + str(overall_full_time / 60 / 60 / 24) # / 1000
print "ORT " + str(overall_reduced_time/60/60/24)
print 1 - overall_reduced_time/overall_full_time/10