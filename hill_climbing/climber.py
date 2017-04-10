__author__ = 'dmitrii'

import csv
import random
from tools.format import featureFormat, targetFeatureSplit
import numpy as np

class Climber:
    dict = []
    features_list = ["EN", "TR", "FR"]
    features_list2 = ["TIM", "TR", "FR"]
    features = []
    target = []
    target2 = []
    threads = []
    freqs = []
    measured = {}
    naive_energy = 0
    naive_time = 0
    sol = 0
    result_set = []
    energy_savings = 0
    time_savings = 0
    def __init__(self, file_name, data_type):
        self.features = []
        self.target = []
        self.target2 = []
        self.threads = []
        self.freqs = []
        self.measured = {}
        self.naive_energy = 0
        self.naive_time = 0
        self.sol = 0
        self.result_set = []
        self.energy_savings = 0
        self.time_savings = 0
        param_list = {'app': "app4", 'flac': "cr_audio1.flac", 'wav': "cr_audio1.wav",
                                          'enw8': "enwik8", 'enw9': "enwik9", 'game': "game1",
                                          '01': "01",'02': "02",'03': "03",'04': "04",'05': "05",'06': "06",'07': "07",
                                          '08': "08",'09': "09",'10': "10",'11': "11",'12': "12",'13': "13",'14': "14",
                                          '16': "16",'17': "17",'18': "18",'19': "19",'20': "20",'21': "21",'22': "22", 'sort':"sort"}
        with open(file_name, 'r') as csv_file:
            reader = csv.DictReader(csv_file)
            for row in reader:
                if row["Name"] == param_list[data_type]:
                    self.dict.append(row)

        data = featureFormat(self.dict, self.features_list)
        self.target, self.features = targetFeatureSplit( data )
        data2 = featureFormat(self.dict, self.features_list2)
        self.target2, features2 = targetFeatureSplit( data2 )
        threads = set()
        freqs = set()
        for f, t in self.features:
            threads.add(f)
            freqs.add(t)
        self.threads = list(threads)
        self.freqs = list(freqs)
        self.threads.sort()
        self.freqs.sort()
        self.naive(file_name, data_type, param_list)
        self.climb()
        self.gain_calculator(file_name,data_type,param_list)
        return



    def climb(self, sol=0):
        neighbor_threads = []
        neighbor_freqs = []
        neighbors = []
        if sol == 0:
            thread = random.randint(0, len(self.threads)-1)
            freq = random.randint(0, len(self.freqs)-1)
            sol = [self.threads[thread], self.freqs[freq]]

        else:
            for i in xrange(len(self.threads)):
                if self.threads[i] == sol[0]:
                    thread = i
            for i in xrange(len(self.freqs)):
                if self.freqs[i] == sol[1]:
                    freq = i
        # print "START OF METHOD"
        # print sol

        if thread != 0 and thread != len(self.threads)-1:
            neighbor_threads.append(self.threads[thread-1])
            neighbor_threads.append(self.threads[thread+1])
            neighbor_threads.append(self.threads[thread])
        if thread == 0:
            neighbor_threads.append(self.threads[thread+1])
            neighbor_threads.append(self.threads[thread])
        if thread == len(self.threads)-1:
            neighbor_threads.append(self.threads[thread-1])
            neighbor_threads.append(self.threads[thread])


        if freq != 0 and freq != len(self.freqs)-1:
            neighbor_freqs.append(self.freqs[freq-1])
            neighbor_freqs.append(self.freqs[freq+1])
            neighbor_freqs.append(self.freqs[freq])
        if freq == 0:
            neighbor_freqs.append(self.freqs[freq+1])
            neighbor_freqs.append(self.freqs[freq])
        if freq == len(self.freqs)-1:
            neighbor_freqs.append(self.freqs[freq-1])
            neighbor_freqs.append(self.freqs[freq])

        for f in neighbor_freqs:
            for t in neighbor_threads:
                neighbors.append([t,f])

        energies = {}
        for i in xrange(len(self.features)):
            for n in neighbors:
                if np.setdiff1d(self.features[i], np.array(n)).size == 0:
                    energies[tuple(n)] = self.target[i]
                    self.measured[tuple(n)] = tuple([self.target[i], self.target2[i]])

        # if self.sol == min(energies, key=energies.get):
        #     # print "***********"
        #     # print "FINISH"
        #     # print min(energies, key=energies.get)
        #     # print energies
        #     #print self.measured
        #     print len(self.measured)
        if self.sol != min(energies, key=energies.get):
            self.sol = min(energies, key=energies.get)
            # print "GOT MINIMUM "
            # print self.sol
            # print energies
            self.climb(min(energies, key=energies.get))

        return

    def naive(self, file_name, data_type, param_list):
        with open(file_name, 'r') as csv_file:
            reader = csv.DictReader(csv_file)
            for row in reader:
                if row["Name"] == param_list[data_type]:
                    if float(row["FR"])== 2900. and int(row["TR"])==32:
                    #if float(row["FR"])== 2900. and int(row["TR"])==32:
                        #print "found"
                        self.naive_energy = float(row["EN"])
                        self.naive_time = float(row["TIM"])
        return

    def gain_calculator(self, file_name, data_type, param_list):
        self.energy_savings = str(round((1 - (self.measured[self.sol][0] / self.naive_energy))*100,2))
        if self.measured[self.sol][1] <= self.naive_time:

            self.time_savings = str(round((1 - self.measured[self.sol][1] / self.naive_time)*100,2))
        else:
            self.time_savings = "-"+str(round((self.measured[self.sol][1] / self.naive_time - 1)*100,2))


        return