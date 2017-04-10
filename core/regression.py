__author__ = 'dmitrii'

import sys
import re
import csv
from sklearn import cross_validation
from sklearn.linear_model import LinearRegression, Ridge
from tools.format import featureFormat, targetFeatureSplit
from sklearn.preprocessing import PolynomialFeatures
from sklearn.pipeline import Pipeline
import random
from mpl_toolkits.mplot3d import Axes3D

import numpy as np

#TODO: comparing to a random version need to throw away old indices staff; change random to specific(see paper)

class Regression:
    dict = []
    features_list = ["EN", "TR", "FR"]
    test_color = "r"
    train_color = "b"
    features = []
    indices = []
    r2 = 0
    r2_actual = 0
    # feature_train = []
    # target_train = []
    # feature_test = []
    # target_test = []



    def __init__(self, file_name, train_size, target, features, indices):
        del self.dict[:]
        del self.indices[:]
        for i in indices:
            self.indices.append(i)

        subset_target = []
        subset_features = []
        for i in self.indices:
            subset_target.append(target[i])
            subset_features.append(features[i])

        self.train_size = train_size

        '''
        kf = cross_validation.KFold(n=len(data), n_folds=10, shuffle=True )
        for train_index, test_index in kf:
            for i in train_index:
                self.feature_train.append(features[i])
                self.target_train.append(target[i])
            for i in test_index:
                self.feature_test.append(features[i])
                self.target_test.append(target[i])
        '''
        # print subset_target
        # print "***************"
        # print subset_features
        self.feature_train, self.feature_test, self.target_train, self.target_test = \
        cross_validation.train_test_split(subset_features, subset_target, train_size=train_size)
        old_indices = []
        return


    def regression(self, filename, param, degree, r2_min, target, features):

        model = Pipeline([('poly', PolynomialFeatures(degree=degree, interaction_only=False)), ('reg',Ridge())])
        #
        # print self.feature_train
        # print self.target_train

        print self.feature_train
        model.fit(self.feature_train, self.target_train)

        r2 = model.score(self.feature_test, self.target_test)
        self.r2 = r2
        print(filename)
        print(param)
        print(degree)
        print(r2)
        print(r2_min)
        if (r2 > r2_min):
            f = open("output_"+str(degree)+".txt", "ab")
            f.write(filename+"\n")
            f.write(param+"\n")
            f.write("Training size = " + str(self.train_size) + "\n")
            f.write("Degree = " + str(degree)+ "\n")
            for i in xrange(degree+1):
                if i == 0:
                    f.write("(TR ^ 0) * (FR ^ 0) = " + str(model.named_steps['reg'].coef_[i]) + "\n")
                else:
                    for j in xrange(i+1):
                        f.write("(TR ^ " + str(i - j) + ") * (FR ^ " + str(j) + ") = " + \
                            str(model.named_steps['reg'].coef_[self.sum_fact(i)+j])+ "\n")

            f.write("R^2 = " + str(model.score(self.feature_test, self.target_test))+"\n")
            f.write("Intercept = " + str(model.named_steps['reg'].intercept_)+"\n")
            # self.draw3D(model)


            self.r2_actual = self.resplit_retest(f=f, model=model, target=target, features=features)
            self.ind_len = len(self.indices)
            f.close()
            self.model = model
            data = []

            with open("tmp"+filename[4:-8]+"_"+param+".csv", 'r') as csv_file:
                reader = csv.DictReader(csv_file)
                for row in reader:
                    data.append(row)
            with open("subsets/"+filename[4:-4]+"_"+param+"_"+str(len(self.indices))+".csv", 'ab') as result:
                fieldnames = data[0].keys()
                writer = csv.DictWriter(result, dialect='excel', fieldnames= fieldnames)
                writer.writeheader()
                for i in xrange(len(data)):
                    if self.indices.__contains__(i):
                        writer.writerow(data[i])

            return True
        return False

    def find_optimal(self, features):
        freqs = [1200., 1300., 1400., 1600., 1700., 1800., 1900., 2000., 2200., 2300., 2400., 2500., 2700., 2800., 2900., 2901.]
        threads = [1., 2., 4., 8., 16., 32.]
        # threads = [1.,2.,3.,4.,5.,6.,7.,8.,9.,10.,11.,12.,13.,14.,15.,16.,17.,18.,19.,20.,21.,22.,23.,24.,25.,26.,27.,28.,29.,30.,31.,32.]
        #print self.model.decision_function(features)
        #print len(features)
        val, idx = min((val,idx) for (idx,val) in enumerate(self.model.decision_function(features)))
        #print val
        #print idx
        #val_act, idx_act = min((val_act,idx_act) for (idx_act,val_act) in enumerate(target))
        #print val_act
        #print idx_act
        #print features[idx_act]
        #print features[idx]
        #print self.model.decision_function(features)[idx_act]
        return val, features[idx]
            #for f in freqs:
            #    for t in threads:
            #        if f == 1200. and t == 1.:
            #            optimal_energy = self.model.predict(np.array([t,f]))[0]
            #            optimal_config = np.array([t,f])
            #            #print optimal_energy
            #            continue
            #        en = self.model.predict(np.array([t,f]))[0]
            #        #print en
            #        if en < optimal_energy:
            #            optimal_energy = en
            #            optimal_config = np.array([t,f])

            #print optimal_config
            #print optimal_energy
            #return optimal_energy, optimal_config

    def get_all_configs(self,features):
        result = []
        for idx, val in enumerate(self.model.decision_function(features)):
            result.append(tuple([features[idx],val]))
        return result

    def draw3D(self, model, feature_test = [], target_test = []):
        import matplotlib.pyplot as plt
        from matplotlib.ticker import LinearLocator, FormatStrFormatter
        from matplotlib import cm
        #reg = model.named_steps['reg']
        fig = plt.figure(1)
        ax = fig.add_subplot(111, projection="3d")
        trained = {}
     
        for xs, zs in zip(self.feature_train, self.target_train):
			if xs[0] > 10.:
				ax.scatter(xs[0], xs[1], zs, c='b', label="train")
        if len(feature_test) == 0 and len(target_test) == 0:
            for xs, zs in zip(self.feature_test, self.target_test):
				if xs[0] > 10.:
					ax.scatter(xs[0], xs[1], zs, c='r' , label="test")
        else:
            for xs, zs in zip(feature_test, target_test):
				if xs[0] > 10.:
					ax.scatter(xs[0], xs[1], zs, c='r' , label="test")
        #ax.scatter(self.target_test, self.feature_test[0], self.feature_test[1], self, c = 'r')
        ax.set_xlabel('Number of threads')
        ax.set_ylabel('Frequency')
        ax.set_zlabel('Energy')

        try:
            #fig = plt.figure(2)
            #bx = fig.gca(projection="3d")
            x = []
            y = []
            z = []
            # y = np.empty(len(self.feature_train))
            # z = np.empty(len(model.predict(self.feature_test)))
            #z_plot = reg.predict()
            if len(feature_test) == 0:
                for xs, zs in zip(self.feature_train, model.predict(self.feature_test)):
                    #bx.plot_trisurf(xs[0], xs[1], zs)
                    x.append(xs[0])
                    y.append(xs[1])
                    z.append(zs)
            else:
                for xs, zs in zip(self.feature_train, model.predict(feature_test)):
                    #bx.plot_trisurf(xs[0], xs[1], zs)
                    x.append(xs[0])
                    y.append(xs[1])
                    z.append(zs)
            # X, Y = np.meshgrid(np.array(x), np.array(y))
            # Z = np.array(z)
            # print X.shape
            # print Z.shape
            # Z = Z.reshape(X.shape)
            #Z = np.meshgrid(np.array(z))
            #print Z


            #comment mot to plot regression surface
             #surf = ax.plot_trisurf(x, y, z, cmap=cm.coolwarm, linewidth=1)
             #ax.zaxis.set_major_locator(LinearLocator(10))
             #ax.zaxis.set_major_formatter(FormatStrFormatter('%.02f'))
             #fig.colorbar(surf, shrink=0.5, aspect=5)



            #plt.plot( self.feature_test[], reg.predict(self.feature_test) )
        except NameError:
            pass

       #a plt.legend()
        plt.show()
        return

    def draw(self, reg):
        import matplotlib.pyplot as plt
        for feature, target in zip(self.feature_test, self.target_test):
            plt.scatter( feature, target, color=self.test_color )
        for feature, target in zip(self.feature_train, self.target_train):
            plt.scatter( feature, target, color=self.train_color )

        ### labels for the legend
        plt.scatter(self.feature_test[0], self.target_test[0], color=self.test_color, label="test")
        plt.scatter(self.feature_test[0], self.target_test[0], color=self.train_color, label="train")




        ### draw the regression line, once it's coded
        try:
            plt.plot( self.feature_test, reg.predict(self.feature_test) )
        except NameError:
            pass
        reg.fit(self.feature_test, self.target_test)
        plt.plot(self.feature_train, reg.predict(self.feature_train), color="r")
        print(reg.coef_)
        plt.xlabel(self.features_list[1])
        plt.ylabel(self.features_list[0])
        plt.legend()
        plt.show()


    def sum_fact(self, num): return reduce(lambda x,y: x+y, range(1 ,num + 1))

    def resplit_retest(self, f, model, target, features):
        # data = featureFormat(self.dict, self.features_list)
        # target, features = targetFeatureSplit( data )
        # self.indices.sort(reverse=True)
        # if len(self.indices) != len(target):
        #     for i in self.indices:
        #         #print len(target)
        #         del target[i]
        #         del features[i]
        # #print len(target)
        #     r2 = model.score(features, target)
        # else:
        #     r2 = model.score(self.feature_test, self.target_test)

        r2 = model.score(features, target)
        f.write("****************\n")
        f.write("R2 for all data = " + str(r2) + "\n")
        #self.draw3D(model, features, target)
        return r2


