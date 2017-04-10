__author__ = 'dmitrii'

import numpy as np
import sys
from random import randint

#TODO: make 3 tests: 11/13/15%; if exists r2 > 90% - take this result; else if: r2<0.85 - cancel; else: take highest possible out of three
#TODO: worst case: 374 runs = 0.39 from total
#TODO: reuse data from smaller subsets: 0.15 from total

def addNaive(features, picked_features):
    for f in features:
        if f[1] == 2900. and f[0] == 32:
            picked_features.add(tuple(f))
def specialCase(data_amount, freqs, threads, features, picked_features):
    repeats = 10
    first_diagonal = []
    for i in xrange(len(freqs)):
        pl = i
        if pl < 6:
            for f in features:
                if f[1] == freqs[i] and f[0] == threads[pl]:
                    first_diagonal.append(f)
        if pl / 6 > 0 and pl / 12 == 0:
            #threads[pl -6 ]
            for f in features:
                if f[1] == freqs[i] and f[0] == threads[pl -6 ]:
                    first_diagonal.append(f)
        if pl / 12 > 0:
            #threads[pl - 12]
            for f in features:
                if f[1] == freqs[i] and f[0] == threads[pl -12 ]:
                    first_diagonal.append(f)
    for i in xrange(repeats):
        picked_features.append(first_diagonal[0])
    for i in xrange(repeats):
        picked_features.append(first_diagonal[int(round(len(first_diagonal)/2.))])
        #picked_features.append(first_diagonal[-1:][0])
    #picked_features.pop(-8)
    for i in xrange(data_amount-3):
        is_in_picked_features = False
        for d in first_diagonal:
            for pf in picked_features:
                if np.setdiff1d(np.array(d), pf).size == 0:
                    is_in_picked_features = True

            if not is_in_picked_features:
                # for i in xrange(10):
                for i in xrange(repeats): #TODO:Workaround!
                    picked_features.append(np.array(d))

            if is_in_picked_features:
                if i < data_amount-3:
                    is_in_picked_features = False
                    # print i
                continue
            else:
                break

    return

def buildDiagonal(number_of_diagonal, main, minor, features, picked_features, configs=0, alternative=None):
    if number_of_diagonal < len(minor)/2:
        start_config = [0, number_of_diagonal * 2]
    else:
        start_config = [0,(number_of_diagonal - len(minor)/2)*2+1]
    was_measured = 0
    configs_in_previous_levels = 0
    if configs == 0:
        configs = len(main)
    iter_configs = iter(xrange(configs))


    for config in iter_configs:
        print(number_of_diagonal)
        print(start_config[1])
        print(config)
        print(start_config[1]+2*config)
        print("Configs in previous level "+str(configs_in_previous_levels))

        print("****************" + str(config) + "***************************")
        # one before border

        first_part = True if configs_in_previous_levels == 0 else False
        if first_part == True:
            one_before_border_test= minor[start_config[1]+2*config - 2 * configs_in_previous_levels]
            border_indicator = config - 2 * configs_in_previous_levels
        else:
            one_before_border_test = minor[start_config[1]+2*config - int(2*(configs_in_previous_levels + start_config[1]/2))]
            border_indicator = config - int(2*(configs_in_previous_levels + start_config[1]/2))
        print(border_indicator)

        if one_before_border_test == minor[len(minor)-2] and alternative != None:
            if config < (len(main)-1)-1:
                if picked_features.__contains__(tuple(list(reversed([main[start_config[0]+config], one_before_border_test])))):
                    was_measured += 1
                if picked_features.__contains__(tuple(list(reversed([alternative[start_config[0]+config], minor[len(minor)-1]])))):
                    was_measured += 1
                picked_features.add(tuple(list(reversed([main[start_config[0]+config], one_before_border_test]))))
                picked_features.add(tuple(list(reversed([alternative[start_config[0]+config], minor[len(minor)-1]]))))
                try:
                    next(iter_configs)
                except StopIteration:
                    break
                configs_in_previous_levels += config + 2 - configs_in_previous_levels
                print("****************" + str(configs_in_previous_levels) + "***************************")
                print("|||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||")
                continue
            if config == (len(main)-1)-1:
                # if tuple(list(reversed([main[config], minor[start_config[1]+2*config - int(2*(configs_in_previous_levels + start_config[1]/2.))]]) == tuple([32.,2900.]):
                #     naive = True
                #     continue
                if picked_features.__contains__(tuple(list(reversed([main[start_config[0]+config], one_before_border_test])))):
                    was_measured +=1
                if picked_features.__contains__(tuple(list(reversed([main[start_config[0]+config+1], minor[len(minor)-1]])))):
                    was_measured +=1
                picked_features.add(tuple(list(reversed([main[start_config[0]+config], one_before_border_test]))))
                picked_features.add(tuple(list(reversed([main[start_config[0]+config+1], minor[len(minor)-1]]))))
                configs_in_previous_levels += config + 2 - configs_in_previous_levels
                print("****************" + str(configs_in_previous_levels) + "***************************")
                print("|||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||")
                break



        # border

        first_part = True if configs_in_previous_levels == 0 else False
        if first_part == True:
            border_test= minor[start_config[1]+2*config - 2 * configs_in_previous_levels]
        else:
            border_test = minor[start_config[1]+2*config - int(2*(configs_in_previous_levels + start_config[1]/2))]

        if border_test == minor[len(minor)-1] and alternative!=None:
            if picked_features.__contains__(tuple(list(reversed([main[start_config[0]+config], minor[len(minor)-1]])))):
                was_measured+=1
            picked_features.add(tuple(list(reversed([main[start_config[0]+config], minor[len(minor)-1]]))))
            configs_in_previous_levels += config + 1 - configs_in_previous_levels
            continue



        #normal case
        if alternative != None:
            first_part = True if configs_in_previous_levels == 0 else False
            if first_part == True:
                general_test = minor[start_config[1]+2*config - 2 * configs_in_previous_levels]
            else:
                print(start_config[1]+2*config - int(2*(configs_in_previous_levels + start_config[1]/2)))
                general_test = minor[start_config[1]+2*config - int(2*(configs_in_previous_levels + start_config[1]/2))]

            if picked_features.__contains__(tuple(list(reversed([main[start_config[0]+config], general_test])))):
                was_measured+=1
            picked_features.add(tuple(list(reversed([main[start_config[0]+config], general_test]))))
        else:
            first_part = True if configs_in_previous_levels == 0 else False
            if first_part == True:
                print("Config " +  str(start_config[1] + 2 * config - 2 * configs_in_previous_levels))
                general_test = minor[start_config[1] + 2 * config - 2 * configs_in_previous_levels]
                if alternative == None and (one_before_border_test == minor[len(minor) - 2] or border_test == minor[len(minor) - 1]):
                        configs_in_previous_levels += config + 1 - configs_in_previous_levels
            else:
                print("Config " +  str(start_config[1] + 2 * config - int(2 * (configs_in_previous_levels + start_config[1] / 2))))
                general_test = minor[start_config[1] + 2 * config - int(2 * (configs_in_previous_levels + start_config[1] / 2))]
                if alternative == None and (one_before_border_test == minor[len(minor) - 2] or border_test == minor[len(minor) - 1]):
                    configs_in_previous_levels += config + 1 - configs_in_previous_levels

            if picked_features.__contains__(tuple(list(reversed([main[start_config[0] + config], general_test])))):
                was_measured += 1
            picked_features.add(tuple(list(reversed([main[start_config[0] + config], general_test]))))
            print(tuple(list(reversed([main[start_config[0] + config], general_test]))))
            # dirty-dirty hack
            #was_measured = 2*config + was_measured


    # print picked_features
    # print main
    # print minor
    # sth = list(picked_features)
    # lst = []
    # for t in sth:
    #     lst.append(list(t))
    # # #print lst
    # for t in lst:
    #     if t[1] == 2901.:
    #         t[1]  = 3000.
    #         t = tuple(t)
    # import pandas
    # df = pandas.DataFrame(lst)
    # df.plot(x = 0, y = 1, ylim = (1200.,3000.), xlim = (1, 32.), kind="scatter")
    # import matplotlib.pyplot as plt
    # plt.xlabel("Small factor")
    # plt.ylabel("Large factor")
    # plt.show()
    print("WAS MEASURED " + str(was_measured))
    return was_measured

def addConfigs(data_amount, main, minor, features, picked_features, alternative=None):
    diagonals_number = data_amount / len(main)
    left_configs = data_amount % len(main)
    #for config in xrange(data_amount):

    for d in xrange(diagonals_number):
        more_configs = buildDiagonal(number_of_diagonal=d, main=main, alternative=alternative, minor=minor, features=features, picked_features=picked_features)
        left_configs += more_configs
        print("More CONFIG " + str(more_configs))
    if left_configs > 0:
        print("LEFT CONFIG " + str(left_configs))

        buildDiagonal(number_of_diagonal=diagonals_number, main=main,alternative=alternative,
                                     minor=minor,features=features,picked_features=picked_features,
                                     configs=left_configs)
        # if alternative == None:
        #     left_configs += more_configs
        #
        # if left_configs > 0:
        #     buildDiagonal(number_of_diagonal=diagonals_number, main=main, alternative=alternative,
        #                                  minor=minor, features=features, picked_features=picked_features,
        #                                  configs=left_configs)

    print(len(picked_features))

    if alternative != None:
        blank_spaces = 0
        # check which configs were not measured
        for f in picked_features:
            for i in xrange(len(alternative)):
                if f == tuple([minor[len(minor)-1],alternative[i]]):
                    blank_spaces += 1
        #print left_configs
        return(blank_spaces)
    else:
        return 0

def finishMajor(data_amount, main, minor, features, picked_features, alternative=None):
    for maj in main:
        for m in minor:
            if not picked_features.__contains__(tuple([m, maj])):
                picked_features.add(tuple([m, maj]))
                data_amount -= 1
                if data_amount == 0:
                    return

def pickIndexesStrategy(features, data_amount, tests_amount=96):
    freqs = sorted(list(set([features[i][1] for i in xrange(len(features))])))
    threads = sorted(list(set([features[i][0] for i in xrange(len(features))])))
    if len(freqs) >= len(threads):
        major_main = [freqs[2*i] for i in xrange(len(freqs)/2)]
        if len(freqs)%2 == 0:
            major_main.append(freqs[len(freqs)-1])
        major_alternative = sorted(list(set(freqs) - set(major_main)))
        minor = threads

    else:
        major_main = [threads[2*i] for i in xrange(len(threads)/2)]
        if len(threads)%2 == 0:
            major_main.append(threads[len(threads)-1])
        major_alternative = sorted(list(set(threads) - set(major_main)))
        minor = freqs


    # two_freq = [1200., 1400., 1700., 1900., 2200., 2400., 2700., 2900., 2901.]
    # alternative_two_freq = [1300., 1600., 1800., 2000., 2300., 2500., 2800.]
    picked_features = set()

    # if (data_amount)/9 == 0:
    #     addNaive(features=features,picked_features=picked_features)
    #     specialCase(data_amount= data_amount, freqs=main_freqs, threads=threads, features=features, picked_features=picked_features)

    # small
    if data_amount <= len(minor) * len(major_main):
        addNaive(features=features,picked_features=picked_features)
        addConfigs(data_amount=data_amount-1, main=major_main, alternative=major_alternative, minor=minor, features=features, picked_features=picked_features)


    # completely irrelevant
    # if data_amount == len(minor) * len(major_main):
    #     for mn in xrange(len(minor)):
    #         for mj in xrange(len(major_main)):
    #             picked_features.add(tuple([major_main[mj],minor[mn]]))

    if data_amount > len(minor) * len(major_main) and data_amount < len(minor)*(len(major_main)+len(major_alternative)):
        addNaive(features=features, picked_features=picked_features)
        blank_spaces = addConfigs(data_amount=len(minor) * len(major_main)-1, main=major_main, alternative=major_alternative, minor=minor,
                   features=features, picked_features=picked_features)
        if data_amount > len(minor) * len(major_main) + blank_spaces:
            finishMajor(data_amount=blank_spaces, main=major_main, alternative=major_alternative, minor=minor,
                   features=features, picked_features=picked_features)
            addConfigs(data_amount=data_amount - len(picked_features), main=major_alternative, minor=minor, features=features, picked_features=picked_features)
            print(len(picked_features))
            # exit()
        else:
            finishMajor(data_amount=len(minor) * len(major_main) + blank_spaces-data_amount, main=major_main,
                        alternative=major_alternative, minor=minor,
                        features=features, picked_features=picked_features)


    # if (data_amount)%9 >= 0 and data_amount >= 9 and data_amount < 27:
    #     addNaive()
    #     print len(picked_features)
    #     pickDefaultBase(data_amount=data_amount-1, freqs=main, threads=threads, features=features, picked_features=picked_features)
    #     print len(picked_features)
    # if (data_amount)%9 >= 0 and data_amount >= 27 and data_amount <= 54:
    #     addNaive(features=features,picked_features=picked_features)
    #     print len(picked_features)
    #     pickDefaultBase(data_amount=data_amount, freqs=main, threads=threads, features=features, picked_features=picked_features)
    #     print len(picked_features)

    # if (data_amount)%9 >= 0 and data_amount > 54 and data_amount < 96:
    #     for f in main_freqs:
    #         for t in threads:
    #             for feat in features:
    #                 if feat[1] == f and feat[0] == t:
    #                     picked_features.append(feat)
    #
    #     if (data_amount-54)%9 >= 0 and (data_amount-54) >=0 and (data_amount-54) <= 54:
    #         pickDefaultBase(data_amount=(data_amount-54), freqs=alternative, threads=threads, features=features, picked_features=picked_features)

    # print "HERE"
    # print len(minor) * (len(major_main) + len(major_alternative))
    # print features
    if data_amount == len(minor)*(len(major_main)+len(major_alternative)):
        for f in features:
            picked_features.add(tuple(list(f)))

    # for f in picked_features:
    #     print f
    #print picked_features
    return picked_features

def randomPicker(features, data_amount, additional_configs, tests_amount=96):
    picked_features = []
    a_c = np.array(additional_configs)
    a_c.shape = (int(len(additional_configs)/2),2)
    if data_amount == 1:
        addNaive(features=features, picked_features=picked_features)
        additional_configs.append("2900.")
        additional_configs.append("32.")
    if len(a_c) > 0:
        for ac in a_c:
            is_in_picked_features = False
            for pf in picked_features:
                if np.setdiff1d(ac, pf).size == 0:
                    is_in_picked_features = True
            if not is_in_picked_features:
                picked_features.append(ac)
    if data_amount > 1:
        for i in xrange(data_amount-1-len(a_c)):
            while True:
                rand = randint(0,len(features)-1)
                is_in_picked_features = False
                for pf in picked_features:
                    if np.setdiff1d(features[rand], pf).size == 0:
                        is_in_picked_features = True

                if not is_in_picked_features:
                    picked_features.append(features[rand])
                    additional_configs.append(features[rand][0])
                    additional_configs.append(features[rand][1])
                    break


    #print picked_features
    return picked_features

class TechniqueHelper:
    def __init__(self, regs):
        self.regressions = regs
        self.highest_reg = self.regressions[0]

    def add_regression(self, reg):
        self.regressions.append(reg)

    def desicion_maker(self):
        # for r in self.regressions:
        #     if r.r2 < 0.85:
        #         return False, r
        #     if r.r2 >= 0.85 and r.r2 > self.highest_reg.r2:
        #         self.highest_reg = r
        #random
        for r in self.regressions:
            if r.r2 > self.highest_reg.r2:
                self.highest_reg = r

        return True, self.highest_reg

