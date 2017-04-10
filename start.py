__author__ = 'dmitrii'

import sys
from api.api import Api
from tools.csv_split import Splitter
import random
from tools.technique import TechniqueHelper
import csv
from os import walk
import os
from tools.indices import Indices
import numpy as np
from hill_climbing.climber import Climber
from sim_annealing.sim_annealing import SimAnnealing

#TODO: comparing to a random version need to throw away old indices staff    ______checked_______
#TODO: as building graphs for score_configuration calculate difference 1 - (r2_subset - r2_full) ______checked_______
#TODO: rescale graphs 0..1 y_axis, x_axis 28..960   ______checked_______

class PickleObject:
    def __init__(self, regs, name, data_type, figure_num):
        self.regs = regs
        self.name = name
        self.data_type = data_type
        self.figure_num = figure_num

def find_train_size(csv, data_type, r2_min, target, features, indices):
    splitter = Splitter("csvs/" + csv, data_type)
    train_size = 0.2
    #splitter.split(data_type)
    new_filename = splitter.make_csv(csv[:-4], data_type)
    degree = 6
    i = 0
    while train_size < 0.7 and i < 10:
        # print "Train Set = " + str(train_size)
        #print "Data amount = " + str(data_amount)
        # print "R2_min = " + str(r2_min)
        result, reg = \
            Api.start("csvs/" + csv, data_type, train_size, new_filename, degree, r2_min=r2_min, target=target, features=features, indices=indices)
        if result == True:
            # print train_size
            success.add(tuple([csv, data_type]))
            return reg
        if result == False and i == 9:
            i = 0
            train_size +=0.01
        i+=1

def plot_r2(regs, name, data_type, figure_num):
    import matplotlib.pyplot as plt
    import mpl_toolkits.axisartist as AA
    r2 = []
    r2_act = []
    els = []
    for reg in regs:
        r2.append(reg.r2)
        if reg.r2_actual < 0:
            r2_act.append(0.0)
        else:
            r2_act.append(reg.r2_actual)
        els.append(reg.ind_len)

    fig = plt.figure(figure_num)
    ax = AA.Subplot(fig, 1, 1, 1)
    fig.add_subplot(ax)
    ax.set_xlim(7,672)
    ax.set_ylim(0,1)
    plt.plot(els, r2, '-o', color="black", label="Subset of data")
    plt.plot(els, r2_act, '-s', color ="black", label="Full data")
    plt.xlabel("Configuration options")
    plt.ylabel("R^2 score")

    plt.legend(loc=4)
    plt.savefig("score_configuration/" + name[:-4] + "_" + data_type)


    delta = 0
    for i in xrange(len(r2)):
        delta += 1 - (r2[i]-r2_act[i])
    delta /= len(r2)
    with open("evaluation/" + name[:-4] + "_" + data_type, "ab") as f:
        f.write(str(delta))
        #return
def delta(regs, name, data_type):
    r2 = []
    r2_act = []
    els = []
    for reg in regs:
        r2.append(reg.r2)
        if reg.r2_actual < 0:
            r2_act.append(0.0)
        else:
            r2_act.append(reg.r2_actual)
        els.append(reg.ind_len)


# csv_list = ["pbzip2_compress.csv",
#             "pbzip2_decompress.csv",
#             "pigz_compress.csv",
#             "pigz_decompress.csv",
#             "plzip_compress.csv",
#             "plzip_decompress.csv",
#             "nanozip_5_compress.csv",
#             "nanozip_5_decompress.csv",
#             "nanozip_50_compress.csv",
#             "nanozip_50_decompress.csv",
#             "nanozip_default_compress.csv",
#             "nanozip_default_decompress.csv"
# ]

repeats = 10.
csv_list = []
data_type_list = []
csv_list.append(sys.argv[1])
data_type_list.append(sys.argv[2])
data_amount = int(sys.argv[3])
repeated_minus_value = int(sys.argv[4])
max_number_of_configs = int(sys.argv[5])
#hill climbing
#repetitions = int(sys.argv[6])
#print csv_list
additional_configs = []
#except hill climbing
if len(sys.argv) > 6:
    for i in xrange(len(sys.argv) - 6):
        additional_configs.append(float(sys.argv[i+6]))

print(data_amount)
print(repeated_minus_value)

# data_type_list = ['app',
#                   # 'flac',
#                   # 'wav',
#                   # 'enw8',
#                   # 'enw9',
#                   # 'game'
# ]
amounts_of_data = [i for i in range(data_amount,data_amount+1,1)]
#amounts_of_data = [3*i for i in range(1,33,1)]
#amounts_of_data = [i for i in range(1,97,1)]
param_list = {'app': "app4", 'flac': "cr_audio1.flac", 'wav': "cr_audio1.wav",
                                          'enw8': "enwik8", 'enw9': "enwik9", 'game': "game1",
                                          '01': "01",'02': "02",'03': "03",'04': "04",'05': "05",'06': "06",'07': "07",
                                          '08': "08",'09': "09",'10': "10",'11': "11",'12': "12",'13': "13",'14': "14",
                                          '16': "16",'17': "17",'18': "18",'19': "19",'20': "20",'21': "21",'22': "22", 'sort':"sort", 'encrypt':"encrypt", 'decrypt':"decrypt"}
#amounts_of_data.append(1.0)

'''
overall_energy = 0.
overall_reduced = 0.
overall_gain = 0.
overall_naive_energy = 0.

overall_optimal_gain = 0.

overall_time = 0.
overall_reduced_time = 0.

#for c in csv_list:
# with open("csvs/results.csv", 'r') as csv_file:
#     reader = csv.DictReader(csv_file)
#     for row in reader:
#         # if c == "pigz_decompress.csv" and row["Name"] == "cr_audio1.flac":
#         #     continue
#         # if c == "nanozip_50_compress.csv" and row["Name"] == "enwik8":
#         #     continue
#         if float(row["FR"])== 2900. and int(row["TR"])==32:
#             overall_naive_energy+=float(row["EN"])
#             with open("csvs/results.csv", 'r') as csv_file2:
#                 reader2 = csv.DictReader(csv_file2)
#                 tmp_list = []
#                 for r in reader2:
#                     if r["Name"] == row["Name"]:
#                         tmp_list.append(float(r["EN"]))
#                 overall_optimal_gain += float(row["EN"]) - min(tmp_list)

#for c in csv_list:
# with open("csvs/results_full.csv", 'r') as csv_file:
#     reader = csv.DictReader(csv_file)
#     for row in reader:
#         overall_energy+=float(row["EN"])
#         overall_time+=float(row["TIM"])

for dirpath,dirnames,filenames in walk("doc/thesis/measurements/final_near_optimal/full_sort/"):
    # print filenames
    for f in filenames:
        with open("doc/thesis/measurements/final_near_optimal/full_sort/"+f, 'r') as csv_file:
            reader = csv.DictReader(csv_file)
            print f
            for row in reader:

                overall_energy+=float(row["EN"])
                overall_time+=float(row["TIM"])


# with open("../evaluation_results/checkTechnique/compression/gains.txt", 'r') as f:
#     content = f.readlines()
#     for row in content:
#         overall_gain+=float(row)

# for dirpath,dirnames,filenames in walk("doc/thesis/measurements/final_near_optimal/subsets_dbs/"):
#     for f in filenames:
#         with open("doc/thesis/measurements/final_near_optimal/subsets_dbs/"+f, 'r') as csv_file:
#             reader = csv.DictReader(csv_file)
#             for row in reader:
#                 print f
#                 overall_reduced+=float(row["EN"])
#                 overall_reduced_time+=float(row["TIM"])


print "OE " + str(overall_energy)
# print "OR" + str(overall_reduced)
# print 1 - overall_reduced/overall_energy

print "\nOT " + str(overall_time/1000/60/60/24)
# print "ORT" + str(overall_reduced_time/60/60/24)
# print 1 - overall_reduced_time/overall_time

#print "\nOG" + str(overall_gain)
# print "ON" + str(overall_naive_energy)
#print overall_gain/overall_naive_energy

# print "\nOOG" + str(overall_optimal_gain)
# print overall_optimal_gain/overall_naive_energy
#
# print 1-(1- overall_optimal_gain/overall_naive_energy)/(1-overall_gain/overall_naive_energy)

'''

left = set()
for c in csv_list:
    for d in data_type_list:
        left.add(tuple([c, d]))

success = set()
r2_min = 0.99
regs = []
while (left - success).__len__() != 0:
    for dt in data_type_list:
        for l in (left - success):

            if l[1] == dt:

                '''
                climbers = []

                for i in xrange(repetitions):
                    climbers.append(SimAnnealing(file_name="csvs/"+l[0], data_type=l[1]))

                combined_measured = {}
                for i in xrange(repetitions):

                    if i == 0:
                        combined_measured = climbers[i].measured
                        near_opt = climbers[i].measured[climbers[i].sol][0]
                        near_opt_climber = climbers[i]
                    else:
                        combined_measured.update(climbers[i].measured)
                        if near_opt > climbers[i].measured[climbers[i].sol][0]:
                            near_opt = climbers[i].measured[climbers[i].sol][0]
                            near_opt_climber = climbers[i]
                #print near_opt_climber.measured
                #print l
                near_opt_climber.result_set.append(["csvs/"+l[0][:-4], param_list[l[1]], repetitions, str(near_opt_climber.sol[0]), str(near_opt_climber.sol[1]),
                           near_opt_climber.energy_savings, near_opt_climber.time_savings, str(near_opt_climber.measured[near_opt_climber.sol][0]),
                                                    str(round(len(combined_measured)/96., 2)), str(sum(v[0] for v in combined_measured.itervalues())*9.),
                                                    str(sum(v[1] for v in combined_measured.itervalues())*9.)])
                with open('sim_annealing_encrypt_01.csv', 'ab') as result:
                            writer = csv.writer(result, dialect='excel')
                            writer.writerows(near_opt_climber.result_set)
                #print combined_measured.values()
                #print near_opt_climber.result_set
                #print round(len(combined_measured)/96., 2)
                exit(0)
                '''

                del regs[:]
                for a in amounts_of_data:
                    indObj = Indices(file_name="csvs/"+l[0], data_type=l[1], data_amount=a, additional_configs=additional_configs, max_number_of_configs=max_number_of_configs)
                    target = indObj.target
                    features = indObj.features
                    indices = indObj.indices


                    r2_min = 0.99
                    # if len(regs) == 0:
                    #     old_indices = []
                    #
                    # else:
                    #     old_indices = []
                    #     for i in regs[len(regs)-1].indices:
                    #         old_indices.append(i)

                    reg = find_train_size(csv=l[0], data_type=l[1], r2_min=r2_min, target=target, features=features, indices=indices)

                    while reg == None:
                        r2_min -=0.01
                        reg = find_train_size(csv=l[0], data_type=l[1], r2_min=r2_min, target=target, features=features, indices=indices)
                    if reg == 0:
                        break
                    regs.append(reg)

                    # if a < 3:
                    #     print features
                    # else:
                    #     exit(0)
                if len(regs) == len(amounts_of_data):


                    #print regs

                    # print regs
                    helper = TechniqueHelper(regs)
                    flag, optimal_regression = helper.desicion_maker()

                    if flag:
                        # print "R^2 = " + str(optimal_regression.r2)
                        # print "R^2 actual = " + str(optimal_regression.r2_actual)
                        optimal_energy, optimal_config = optimal_regression.find_optimal(features)
                        print(optimal_energy)
                        if optimal_energy < 0:
                            # print "Please restart!"
                            f = open("to_restart.txt", "ab")
                            f.write(l[0]+ " " + l[1]+"\n")
                            f.close()
                            print(sys.argv)
                            if repeated_minus_value >= 10:
                                sys.argv[4] = str(1)
                                sys.argv[3] = str(int(sys.argv[3]) + 1)
                                sys.argv[5] = str(max_number_of_configs)
                                sys.argv[2] = dt
                                sys.argv[1] = l[0]
                                #if len(sys.argv) > 6:
                                #    # for i in xrange(len(sys.argv) - 6):
                                #    del sys.argv[-(len(sys.argv) - 6):]
                            else:
                                sys.argv[2] = dt
                                sys.argv[1] = l[0]
                                sys.argv[4] = str(int(sys.argv[4]) + 1)
                            python = sys.executable
                            print(sys.argv)
                            os.execl(python, python, * sys.argv)
                            #sys.exit()
                        # print l[0]
                        # print l[1]
                        with open("csvs/"+l[0], 'r') as csv_file:
                            python = sys.executable
                            res = []
                            time_naive = []
                            near_opt_res = []
                            near_opt_time = []
                            fin_res = 0.
                            fin_near_opt = 0.
                            fin_time_naive = 0.
                            fin_time_near_opt = 0.
                            measured_energies = {}
                            measured_times = {}

                            freqs = list(set([features[i][1] for i in xrange(len(features))]))
                            threads = list(set([int(features[i][0]) for i in xrange(len(features))]))

                            for f in freqs:
                                for t in threads:
                                    measured_energies[tuple([str(f),str(t)])] = 0
                                    measured_times[tuple([str(f),str(t)])] = 0
#	    counter[tuple([str(f),str(t)])] = 0

                            param_list = {'app': "app4", 'flac': "cr_audio1.flac", 'wav': "cr_audio1.wav",
                                          'enw8': "enwik8", 'enw9': "enwik9", 'game': "game1",
                                          '01': "01",'02': "02",'03': "03",'04': "04",'05': "05",'06': "06",'07': "07",
                                          '08': "08",'09': "09",'10': "10",'11': "11",'12': "12",'13': "13",'14': "14",
                                          '16': "16",'17': "17",'18': "18",'19': "19",'20': "20",'21': "21",'22': "22", 'sort':"sort", "encrypt":'encrypt', 'decrypt':"decrypt"}
                            reader = csv.DictReader(csv_file)
                            for row in reader:
                                if row["Name"] == param_list[l[1]]:
                                    if float(row["FR"])== 2900. and int(row["TR"])==32:
                                    #if float(row["FR"])== 2900. and int(row["TR"])==32:
                                        res.append(float(row["EN"]))
                                        time_naive.append(float(row["TIM"]))
                                    if float(row["FR"])== optimal_config[1] and int(row["TR"])==optimal_config[0]:
                                    #if float(row["FR"])== optimal_config[1] and int(row["TR"])==optimal_config[0]:
                                        near_opt_res.append(float(row["EN"]))
                                        near_opt_time.append(float(row["TIM"]))
                                        #print measured_energies.keys()
                                    measured_energies[tuple([row["FR"],row["TR"]])] += float(row["EN"])
                                    measured_times[tuple([row["FR"],row["TR"]])] += float(row["TIM"])

                            for r in res:
                                fin_res += r
                            for r in near_opt_res:
                                fin_near_opt += r

                            for t in time_naive:
                                fin_time_naive += t
                            for t in near_opt_time:
                                fin_time_near_opt += t

                            # gain = (fin_res/repeats) - (fin_near_opt/repeats)
                            gain = (fin_res/repeats) - (fin_near_opt/repeats)

                            print(gain)
                            #brise

                            a_c = np.array(additional_configs)
                            a_c.shape = (int(len(additional_configs)/2),2)
                            for ac in a_c:
                                if np.setdiff1d(optimal_config, ac).size == 0:
                                    os.execl(python, python, * sys.argv)
                            #if gain < 0 and float(data_amount*3+float(len(additional_configs))/2)/(32*3) < 0.4:

                            if gain < 0:
                                f = open("to_restart.txt", "ab")
                                f.write(l[0]+ " " + l[1]+"\n")
                                f.close()
                                #python = sys.executable
                                for i in xrange(len(optimal_config)):
                                    sys.argv.append(str(optimal_config[i]))
                                    print("**************************************")
                                    print(optimal_config[i])
                                    print("**************************************")
                                #random
                                sys.argv[3] = str(int(sys.argv[3]) + 1)

                                sys.argv[4] = str(1)
                                sys.argv[5] = str(max_number_of_configs)
                                os.execl(python, python, * sys.argv)
                            # print "GAIN   "+str(gain)
                            # if gain < 0 and float(data_amount*3+float(len(additional_configs))/2)/(32*3) >= 0.4:
                            #     optimal_config = np.array([32,2900.])
                            #     optimal_energy=fin_res/repeats
                            for i in indices:
                                print("************************")
                                print("TRY")
                                #print measured_energies.keys()
                                print(tuple([str(features[i][1]),str(int(features[i][0]))]))
                                print(measured_energies[tuple([str(features[i][1]),str(int(features[i][0]))])]/repeats)
                                print(fin_near_opt/repeats)
                                print("************************")
                                #TODO: here is the point to check
                                if fin_near_opt/repeats > measured_energies[tuple([str(features[i][1]),str(int(features[i][0]))])]/repeats:
                                    optimal_config = np.array(tuple([str(int(features[i][0])),str(features[i][1])]))
                                    optimal_energy = measured_energies[tuple([str(features[i][1]),str(int(features[i][0]))])]/repeats
                                    fin_near_opt = measured_energies[tuple([str(features[i][1]),str(int(features[i][0]))])]
                                    fin_time_near_opt = measured_times[tuple([str(features[i][1]),str(int(features[i][0]))])]
                            f = open("gains.txt", "ab")
                            f.write(str(gain)+"\n")
                            f.close()

                        resultSet = []

                        energy_savings = str(round((1 - (fin_near_opt/repeats) / (fin_res/repeats))*100,2))
                        if fin_time_near_opt/repeats <= fin_time_naive/repeats:
                            time_savings = str(round((1 - (fin_time_near_opt/repeats) / (fin_time_naive/repeats))*100,2))
                        else:
                            time_savings = "-"+str(round(((fin_time_near_opt/repeats) / (fin_time_naive/repeats) - 1)*100,2))
                        #brise
                        # resultSet.append([l[0][:-4], param_list[l[1]], str(optimal_config[0]), str(optimal_config[1]),
                        #                    energy_savings, time_savings, str(fin_near_opt/repeats), str(float(data_amount*3+float(len(additional_configs))/2)/(32*3))])
                        #fedorov
                        resultSet.append([l[0][:-4], param_list[l[1]], str(optimal_config[0]), str(optimal_config[1]),
                                           energy_savings, time_savings, str(fin_near_opt/repeats), str(float(data_amount+float(len(additional_configs))/2)/(32*3))])
                        #random
                        # resultSet.append([l[0][:-4], param_list[l[1]], str(optimal_config[0]), str(optimal_config[1]),
                        #                    energy_savings, time_savings, str(fin_near_opt/repeats), str(float(float(len(additional_configs))/2)/(32*3))])
                        #resultSet.append([l[0][:-4], str(optimal_config[0]), str(optimal_config[1]),
                        #                  energy_savings, time_savings, str(fin_near_opt/repeats), str(float(data_amount*3+float(len(additional_configs))/2)/(32*3))])
                        with open('near_optimal.csv', 'ab') as result:
                            writer = csv.writer(result, dialect='excel')
                            writer.writerows(resultSet)



                    else:
                        # print "Insufficient!"
                        f = open("insufficient.txt", "ab")
                        f.write(l[0]+ " " + l[1]+"\n")
                        f.close()
                    '''


                    import pickle
                    pkl = PickleObject(regs=regs, name=l[0], data_type=dt, figure_num=random.randrange(0, 1000))
                    output = open("pickles/" +l[0][:-4]+"_"+dt+".pkl", 'ab')
                    pickle.dump(pkl, output, 0)
                    del pkl
                    #plot_r2(regs=regs, name=l[0], data_type=dt, figure_num=figure_num)
                    output.close()
                    print regs
                    '''

#
# import pickle, pprint
# data2 = []
# for dirpath,dirnames,filenames in walk("pickles/"):
#     for f in filenames:
#         with open("pickles/"+f, 'r') as pkl_file:
#             pkl = pickle.load(pkl_file)
#             data2.append(pkl)
# print data2
# for d in data2:
#     print d.regs
#     plot_r2(regs=d.regs, name=d.name, data_type=d.data_type, figure_num=d.figure_num)
#
# pkl_file.close()

'''
import pickle, pprint
data2 = []
with open("pickles/pbzip2_compress_app.pkl", 'rb') as pkl_file:
    #for i in range(32):
    pkl = pickle.load(pkl_file)
    data2.append(pkl)
print data2
for d in data2:
    plot_r2(regs=d.regs, name=d.name, data_type=d.data_type, figure_num=d.figure_num)

pkl_file.close()
'''
