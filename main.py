import numpy as np
import math


class naive_bayes:
    fileRoot = 'd:\\naive bayes\\'
    datasetFilename = 'Dataset.dat'
    dataSet = np.array([])
    prop = np.array([])
    mean = np.array([])
    var = np.array([])

    def getDataset(self):
        filePath = self.fileRoot + self.datasetFilename
        fo = open(filePath, 'r')
        line = fo.readline()
        self.prop = np.array(eval(line))
        self.dataSet = self.prop.copy()
        line = fo.readline()
        while line != '':
            self.dataSet = np.row_stack((self.dataSet, np.array(eval(line))))
            line = fo.readline()
        self.dataSet = self.dataSet[1:, :]
        self.dataSet = self.dataSet.astype(np.float64)

    def init(self):
        '''
        Get mean and var
        :return:NONE
        '''
        self.mean = np.array([[float(0) for i in range(len(self.prop) - 1)] for i in range(2)])
        self.var = np.array([[float(0) for i in range(len(self.prop) - 1)] for i in range(2)])
        for i in range(2):
            subdata = self.dataSet[np.where(self.dataSet[:, 0] == i)]
            if i:
                self.mean = np.row_stack((self.mean, np.mean(subdata, 0)))
                self.var = np.row_stack((self.var, np.var(subdata, 0)))
            else:
                self.mean = np.mean(subdata, 0)
                self.var = np.var(subdata, 0)

    def Gauss(self, u, v, x):
        return math.exp(-(x - u) ** 2 / (2 * v)) / math.sqrt(2 * math.pi * v)

    def Classifier(self, sample):
        '''
        :param sample: list[vector] Test sample
        :return: list[_index] Classifier result
        '''
        res = []
        for samplex in sample:
            _Psex = np.array([0.5, 0.5])
            Psex = _Psex
            for sex in range(2):
                for i in range(1, len(self.prop)):
                    Psex[sex] *= self.Gauss(self.mean[sex][i], self.var[sex][i], samplex[i-1])
            print Psex
            print [i / sum(Psex) for i in Psex]
            print np.where(Psex == np.max(Psex))
            res.append(np.where(Psex == np.max(Psex)))
        return res


nb = naive_bayes()
nb.getDataset()
nb.init()
sample = [[6, 130, 8], [6.60, 180, 12], [5.0, 150, 7]]

res = nb.Classifier(sample)

for r in res:
    if r == np.array([1]):
        print 'female'
    else:
        print 'male'
