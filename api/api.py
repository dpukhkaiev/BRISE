__author__ = 'dmitrii'
from core.regression import Regression
from tools.csv_split import Splitter
class Api:
    @staticmethod
    def start(filename, param, train_size, new_filename, degree, r2_min, target, features, indices):



        regression = Regression(new_filename, train_size, target=target, features=features, indices=indices)
        #print old_indices
        return regression.regression(filename, param, degree, r2_min=r2_min, target=target, features=features), regression
