__author__ = 'dmitrii'
import numpy as np
def featureFormat(dictionary, features, sort_keys=False):
    return_list = []
    # if sort_keys:
    #     keys = sorted(dictionary.keys())
    # else:
    #     keys = dictionary.keys()

    for key in xrange(len(dictionary)):
        tmp_list = []
        for feature in features:
            try:
                dictionary[key][feature]
            except KeyError:
                print("error: key ", feature, " not present")
                return
            value = dictionary[key][feature]
            tmp_list.append( float(value) )


        return_list.append( np.array(tmp_list) )

    return return_list

def targetFeatureSplit( data ):
    """
        given a numpy array like the one returned from
        featureFormat, separate out the first feature
        and put it into its own list (this should be the
        quantity you want to predict)

        return targets and features as separate lists

        (sklearn can generally handle both lists and numpy arrays as
        input formats when training/predicting)
        """


    target = []
    features = []
    feature1 = []
    feature2 = []
    # if len(data[0]) <= 2:
    for item in data:
        target.append( item[0] )
        features.append( item[1:] )
    return target, features
    # else:
    #     for item in data:
    #         target.append(item[0])
    #         feature1.append(item[1])
    #         feature2.append(item[2])
    #
    #     return target, feature1, feature2
