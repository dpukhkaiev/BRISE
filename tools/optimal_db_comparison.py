__author__ = 'dmitrii'

import numpy as np
import csv

with open("../csvs/results.csv", 'r') as csv_file:
    query = "22"
    near_opt_freq = 2700.
    near_opt_tr = 8
    res = []
    time_naive = []
    near_opt_res = []
    near_opt_time = []
    fin_res = 0.
    fin_near_opt = 0.
    fin_time_naive = 0.
    fin_time_near_opt = 0.
    #param_list = {'app': "app4", 'flac': "cr_audio1.flac", 'wav': "cr_audio1.wav",
    #              'enw8': "enwik8", 'enw9': "enwik9", 'game': "game1"}
    reader = csv.DictReader(csv_file)
    for row in reader:
        if row["sql"] == query and float(row["FR"])== 2900. and int(row["TR"])==32:
            res.append(float(row["EN"]))
            time_naive.append(float(row["TIM"]))
        if row["sql"] == query and float(row["FR"])== near_opt_freq and int(row["TR"])==near_opt_tr:
            near_opt_res.append(float(row["EN"]))
            near_opt_time.append(float(row["TIM"]))
    for r in res:
        fin_res += r
    for r in near_opt_res:
        fin_near_opt += r

    for t in time_naive:
        fin_time_naive += t
    for t in near_opt_time:
        fin_time_near_opt += t

    gain = (fin_res/10.) - (fin_near_opt/10.)
    print gain


    resultSet = []

    energy_savings = str(round((1 - (fin_near_opt/10.) / (fin_res/10.))*100,2))
    if fin_time_near_opt/10. <= fin_time_naive/10.:
        time_savings = str(round((1 - (fin_time_near_opt/10.) / (fin_time_naive/10.))*100,2))
    else:
        time_savings = "-"+str(round(((fin_time_near_opt/10.) / (fin_time_naive/10.) - 1)*100,2))
    resultSet.append([query, str(near_opt_freq), str(near_opt_tr),
                      energy_savings, time_savings, str(fin_near_opt/10.)])
    with open('near_optimal.csv', 'ab') as result:
        writer = csv.writer(result, dialect='excel')
        writer.writerows(resultSet)
