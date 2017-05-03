# Ronak Kumar (2015080)

import csv
import math
import random
import sys

class naive_bayes:
    
    def __init__(self, data):
        self.data = data

    def split_dset(self, dset):
        split_ratio = 0.80
        train_set_size = int(len(dset) * split_ratio)
        test_set_size = len(dset) - train_set_size
        train_set = []
        test_set = []
        original = dset
        i = 0
        while(i <= train_set_size):
            train_set.append(original[i])
            i += 1
        while(i < len(dset)):
            test_set.append(original[i])
            i += 1
        return[train_set, test_set]

    def load_data_file(self, fname):
        raw_data = csv.reader(open(fname, "rb"))
        dset = list(raw_data)
        for i in range(len(dset)):
            dset[i] = [x for y in dset[i] for x in y.split("  ")]
        for i in range(len(dset)):
            dset[i] = [x for y in dset[i] for x in y.split(" ")]
        for i in range(len(dset)):
            dset[i] = [float(x) for x in dset[i]]
        return dset
    
    def separate_data_by_class(self, dset):
        class_data = {}
        for i in range(len(dset)):
            temp = dset[i]
            if(temp[-1] not in class_data):
                class_data[ temp[-1] ] = []
            class_data[temp[-1]].append(temp)
        return class_data

    def std_dev(self, nums):
        avg = sum(nums) / float(len(nums))
        var = math.sqrt(sum([pow( x - avg , 2) for x in nums ]) / float(len(nums) - 1))
        return var

    def sumrz_by_class(self, dset):
        sumrz = {}
        separated_data = self.separate_data_by_class(dset)
        for cValue, inst in separated_data.iteritems():
            sumrz_temp =  [(sum(x) / float(len(x)), self.std_dev(x)) for x in zip (* dset)]
            del sumrz_temp[-1]
            sumrz [cValue] = sumrz_temp
        return sumrz

    def calculate_the_probability(self, a, mn, std_dev):
        ans = ( 1 / ( math.sqrt ( 2 * math.pi ) * std_dev) ) * math.exp ( - (math.pow (a - mn, 2) / (2 * math.pow ( std_dev, 2) ) ) )
        return ans
    
    def predict_inp(self, sumrz, inp):
        probs = {}
    
        bprob = -1

        b2 = None
		
        for cV,cS in sumrz.iteritems () :
            probs[cV] = 1
            j = 0
            while (j < len(cS)):
                mn, std_dev = cS [j]
                a = inp[j]
                probs [cV]  *= self.calculate_the_probability (a, mn, std_dev)
                j += 1

        for cV , prob in probs.iteritems():
            if b2 is None or prob > bprob:
                bprob = prob
                b2 = cV

        return b2

	
    def calculate_pred(self , sumrz , test_set):
        preds = []
        for i in range(len(test_set)):
            rslt = self.predict_inp(sumrz, test_set[i])
            preds.append ( rslt )
        return preds

    def print_accuracy(self , test_set , preds):
    
        count = 0
        a = 0
        while(a < len(test_set)):
            if test_set[a][-1] == preds[a]:
                count = count + 1
            a = a + 1

        print('Classification Accuracy : {0}%').format((count / float( len( test_set ) ) ) * 100.0)

def main():
    
    # Add the .csv file here. For Example given below
    fname = 'sample.data.csv'
    nbayes = naive_bayes(0)
    dset =  nbayes.load_data_file(fname)
    train_set, test_set = nbayes.split_dset(dset)
    sumrz = nbayes.sumrz_by_class(train_set)
    preds = nbayes.calculate_pred(sumrz, test_set)
    print('For ' + fname + ' dataset Splitted into 80 and 20%')
    nbayes.print_accuracy(test_set, preds)

if __name__ == '__main__':
    main()
