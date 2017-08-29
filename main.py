import numpy as np
import math


class naive_bayes:
    fileRoot = 'D:\Bayes\NaiveBayes\\'
    datasetFilename = 'trainingdata.dat'
    testsetFilename = 'testdata.dat'
    dataSet = np.array([])
    mean = np.array([])
    var = np.array([])
    testSet = list()
    vectorLength = 0

    def __init__(self):
        self.getDataset()
        self.training()
        self.getTestset()

    def getDataset(self):
        '''
        dataSet: training database
        vectorLength:
        :return: NONE
        '''
        filePath = self.fileRoot + self.datasetFilename
        fo = open(filePath, 'r')
        line = fo.readline()
        self.vectorLength = eval(line)
        line = fo.readline()
        while line != '':
            if(self.dataSet.shape[0] > 0):
                self.dataSet = np.row_stack((self.dataSet, np.array(eval(line))))
            else:
                self.dataSet = np.array(eval(line))
            line = fo.readline()
        self.dataSet = self.dataSet.astype(np.float64)

    def getTestset(self):
        filePath = self.fileRoot + self.testsetFilename
        fo = open(filePath, 'r')
        res = list()
        line = fo.readline()
        while line != '':
            res.append(list(eval(line)))
            line = fo.readline()
        self.testSet = res

    def training(self):
        '''
        Get mean and var
        :return:NONE
        '''
        self.mean = np.array([[float(0) for i in range(self.vectorLength)] for i in range(2)])
        self.var = np.array([[float(0) for i in range(self.vectorLength)] for i in range(2)])
        for i in range(2):
            subdata = self.dataSet[np.where(self.dataSet[:, -1] == i)]
            if i:
                self.mean = np.row_stack((self.mean, np.mean(subdata, 0)))
                self.var = np.row_stack((self.var, np.var(subdata, 0)))
            else:
                self.mean = np.mean(subdata, 0)
                self.var = np.var(subdata, 0)
        # print self.mean
        # print self.var
        # exit()


    def Gauss(self, u, v, x):
        return math.exp(-(x - u) ** 2 / (2 * v)) / math.sqrt(2 * math.pi * v)

    def Classifier(self):
        '''
        :param sample: list[vector] Test sample
        :return: list[_index] Classifier result
        '''
        res = list()
        for samplex in self.testSet:
            _Psex = np.array([0.5, 0.5])
            Psex = _Psex
            for sex in range(2):
                for i in range(0, self.vectorLength):
                    Psex[sex] *= self.Gauss(self.mean[sex][i], self.var[sex][i], samplex[i])
            # print Psex
            # print [i / sum(Psex) for i in Psex]
            # print np.where(Psex == np.max(Psex))
            res.append(np.where(Psex == np.max(Psex)))
        return res


nb = naive_bayes()
res = nb.Classifier()

for r in res:
    if r[0] == 1:
        print 'female'
    else:
        print 'male'
