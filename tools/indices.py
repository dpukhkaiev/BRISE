__author__ = 'dmitrii'
import numpy as np
from tools.format import featureFormat, targetFeatureSplit
import csv
from tools.technique import pickIndexesStrategy, randomPicker
import numpy
import os
import random
import re
import geopy
import geopy.distance
from tools.split_list import SplitList
from sys import stdout

class Indices:
    dict = []
    features_list = ["EN", "TR", "FR"]
    features = []
    target = []
    indices = []


    def __init__(self, file_name, data_type, data_amount, additional_configs, max_number_of_configs):
        param_list = {'app': "app4", 'flac': "cr_audio1.flac", 'wav': "cr_audio1.wav",
                                          'enw8': "enwik8", 'enw9': "enwik9", 'game': "game1",
                                          '01': "01",'02': "02",'03': "03",'04': "04",'05': "05",'06': "06",'07': "07",
                                          '08': "08",'09': "09",'10': "10",'11': "11",'12': "12",'13': "13",'14': "14",
                                          '16': "16",'17': "17",'18': "18",'19': "19",'20': "20",'21': "21",'22': "22", 'sort':"sort", 'encrypt':"encrypt", 'decrypt':"decrypt"}
        del self.dict[:]
        del self.indices[:]
        del self.target[:]
        del self.features[:]
        #brise/fedorov
        a_c = np.array(additional_configs)
        a_c.shape = (int(len(additional_configs)/2),2)

        print(data_type)
        self.d_a = data_amount
        with open(file_name, 'r') as csv_file:
            reader = csv.DictReader(csv_file)
            for row in reader:
                if row["Name"] == param_list[data_type]:
                    self.dict.append(row)

        data = featureFormat(self.dict, self.features_list)
        target, features = targetFeatureSplit( data )
        print(len(features))
        print("3")
        print(data_amount)

        #fedorov
        '''
        os.system("Rscript fedorov.R " + str(data_amount))
        r_indices_dict = {}
        freqs = list(set([features[i][1] for i in xrange(len(features))]))
        threads = list(set([int(features[i][0]) for i in xrange(len(features))]))
        num = 1
        for t in threads:
            for f in freqs:
                r_indices_dict[tuple([t,f])] = num
                num += 1
        #print r_indices_dict
        with open("somefile") as file:
            content = file.read()
        r_indices = re.split(" ", content)
        picked_features = []
        for k in r_indices_dict.keys():
            #print r_indices_dict[k]
            if r_indices.__contains__(str(r_indices_dict[k])):
                picked_features.append(numpy.asarray(k))
        '''
        #sobol
        #sort search space
        temp_filename = "somefile_" + str(random.randint(1,1000000)) + ".csv"

        os.system("Rscript sobol.R " + str(max_number_of_configs) + " " + temp_filename)
        all_features = []
        with open(temp_filename, 'r') as csv_file:
            reader = csv.DictReader(csv_file)
            for row in reader:
                all_features.append(tuple(list([float(row["TR"]), float(row["FR"])])))
        all_features.sort(key= lambda  x: x[0])
        split_list = SplitList(all_features, max_number_of_configs/16)
        all_features = split_list.list
        #pick features
        os.system("Rscript sobol.R " + str(data_amount) + " " + temp_filename)
        picked_features = []
        with open(temp_filename, 'r') as csv_file:
            reader = csv.DictReader(csv_file)
            for row in reader:
                picked_features.append(tuple(list([float(row["TR"]),float(row["FR"])])))
        picked_features.pop()
        picked_features.append(tuple(all_features[6-1][15-1]))

        # picked_coords = []
        # for pf in picked_features:
            # for i, row in enumerate(all_features):
            #     try:
            #         picked_coords.append(tuple([i+1, row.index(pf)+1]))
            #     except:
            #         continue
        #    picked_coords.append(tuple(list([int(pf[0])+1,int(pf[1])+1])))
        
        coordinates = []
        tr_list = [i for i in range(1,7,1)]
        fr_list = [i for i in range(1,17,1)]
        for tr in tr_list:
            for fr in fr_list:
                coordinates.append([tr,fr])
        points = [geopy.Point(p[0],p[1]) for p in coordinates]
        picked_coords = []
        for pf in picked_features:
            pf = geopy.Point(pf[0],pf[1])
            all_distances = [(p,geopy.distance.distance(p,pf).km) for p in points]
            i = 0
            while picked_coords.__contains__(sorted(all_distances, key=lambda x: (x[1]))[i][0]):
                i+=1
            picked_coords.append(sorted(all_distances, key=lambda d: (d[1]))[i][0])
        #print picked_features
        # exit()
        picked_features = []
        freqs = [1200., 1300., 1400., 1600., 1700., 1800., 1900., 2000., 2200., 2300., 2400., 2500., 2700., 2800.,
                 2900., 2901.]
        threads = [1., 2., 4., 8., 16., 32.]
        # threads = [1.,2.,3.,4.,5.,6.,7.,8.,9.,10.,11.,12.,13.,14.,15.,16.,17.,18.,19.,20.,21.,22.,23.,24.,25.,26.,27.,28.,29.,30.,31.,32.]

        for pc in picked_coords:
            picked_features.append([threads[int(pc[0])-1],freqs[int(pc[1]) - 1]])
        print picked_features



        #brise
        # picked features should be a set
        #picked_features = pickIndexesStrategy(features=features, data_amount=data_amount)

        #random
        #picked_features = randomPicker(features=features, data_amount=data_amount, additional_configs=additional_configs)
        #print picked_features

        #print "4"
        #print len(picked_features)
        for i in xrange(len(features)):
            self.features.append(features[i])
            self.target.append(target[i])
            for pf in picked_features:
                if np.setdiff1d(features[i], pf).size == 0:
                    self.indices.append(i)
                    break
            # brise/fedorov
            for ac in a_c:
                # print ac
                # print features[i]
                if np.setdiff1d(features[i], ac).size == 0:
                    self.indices.append(i)
                    break
        print(len(self.indices))
        #print self.indices

        #print "5"
