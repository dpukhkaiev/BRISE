__author__ = 'dmitrii'

import re
import sys
import csv
import operator

def optimal_finder():
    name = sys.argv[1]
    f1 = csv.reader(open(name, 'rb'))

    minEnergy = 0
    minRow = []
    energy ={}
    time = {}
    freqs = [1200.0,1300.0, 1400.0, 1600.0, 1700.0, 1800.0, 1900.0, 2000.0, 2200.0, 2300.0, 2400.0, 2500.0, 2700.0, 2800.0, 2900.0, 2901.0]
    threads = [1, 2, 4, 8, 16, 32]
 #   counter = {}
    for f in freqs:
        for t in threads:
            energy[tuple([str(f),str(t)])] = 0	
	    time[tuple([str(f),str(t)])] = 0
#	    counter[tuple([str(f),str(t)])] = 0	    
    
    #print energy.keys()	
    for row in f1:
	if row[0] == "FR":
		continue
	if tuple([row[0],row[6]]) == ('2900.0','32'):
	    print "ENERGY START " + str(energy[tuple([row[0],row[6]])])
	    print "ADD ENERGY " + row[2]
	energy[tuple([row[0],row[6]])] +=float(row[1])
	if tuple([row[0],row[6]]) == ('2900.0','32'):
            print "AFTER ADD " + str(energy[tuple([row[0],row[6]])])
	time[tuple([row[0],row[6]])] +=float(row[7])
#	counter[tuple([row[0],row[4]])] += 1
    #print counter 
    '''
        if minEnergy == 0:
            mainName = "Count-200.0mio_new.csv"
            minEnergy = float(row[2])
            del minRow[:]
            minRow.append(mainName)
            minRow.extend(row)


        if minEnergy > float(row[2]):
            mainName = "Count-200.0mio_new.csv"
            minEnergy = float(row[2])
            del minRow[:]
            minRow.append(mainName)
            minRow.extend(row)
    '''
    print energy[('2900.0','32')]   
    for k in energy.keys():
	#print energy[k]
	energy[k] /= 10.
	time[k] /= 10.

    #print energy
    minEn = min(energy.values())
    for k in energy.keys():
	if energy[k] == minEn and energy[k] != 0:
	    minRow.append(name)
	    minRow.append(k[0])
	    minRow.append(k[1])
	    minRow.append(str(round((1-energy[k]/energy[tuple(['2900.0','32'])])*100.0,2)))
	    if time[k] <=time[tuple(['2900.0','32'])]:
	        minRow.append(str(round(1-(time[k]/time[tuple(['2900.0','32'])])*100.0,2)))
	    else:
		minRow.append("-"+str(round((time[k] / time[tuple(['2900.0','32'])] - 1)*100.0,2)))
	    minRow.append(energy[k])
	    minRow.append(time[k])
    return minRow






header = ["Threads","Frequecy", "EnergySavings", "TimeSavings", "Energy"]
resultSet = []
resultSet.append(header)
i = 0
resultSet.append([])
print optimal_finder()

resultSet.append(optimal_finder())



with open('optimal_energy.csv', 'ab') as result:
    writer = csv.writer(result, dialect='excel')
    writer.writerows(resultSet)


