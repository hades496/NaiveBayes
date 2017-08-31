import math
import collections as cs


class Statistics:
    def getMean(self, data):
        '''

        :param data: a 2d-list
        :param index: Mean of each Row when index==0,Mean of each Col when index==1,
        :return:
        '''
        Row = len(data)
        Col = len(data[0])
        mean = list()
        mean = [0 for _ in range(Col)]
        for i in range(Col):
            try:
                mean[i] += data[0][i]
            except:
                mean[i] = cs.Counter()
            else:
                mean[i] = 0
        for i in range(Row):
            for j in range(Col):
                try:
                    mean[j] += data[i][j]
                except:
                    mean[j].update([data[i][j]])
                else:
                    mean[j] += data[i][j] / float(Col)
        return mean

    def getVar(self, data):
        '''

        :param data: a 2d-list
        :param index: Var of each Row when index==0,Var of each Col when index==1,
        :return:
        '''
        Row = len(data)
        Col = len(data[0])
        var = list()
        mean = self.getMean(data)
        var = [0 for _ in range(Col)]
        for i in range(Row):
            for j in range(Col):
                try:
                    var[j] += (data[i][j] - mean[j]) ** 2
                except:
                    var[j] = 0
                else:
                    var[j] += (data[i][j] - mean[j]) ** 2 / float(Col - 1)
        return var


class naive_bayes(Statistics):
    fileRoot = 'D:\Bayes\NaiveBayes\\'
    datasetFilename = 'trainingdata.dat'
    testsetFilename = 'testdata.dat'
    dataSet = list()
    mean = list()
    var = list()
    testSet = list()
    sexSize = [0.0, 0.0]
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
        self.isnum = list(eval(line))
        line = fo.readline()
        while line != '':
            line = line.split(',')
            for i in range(self.vectorLength + 1):
                if self.isnum[i]:
                    line[i] = int(line[i])
            self.dataSet.append(line)
            line = fo.readline()

    def getTestset(self):
        filePath = self.fileRoot + self.testsetFilename
        fo = open(filePath, 'r')
        line = fo.readline()
        while line != '':
            line = line.strip()
            line = line.split(',')
            for i in range(self.vectorLength):
                if self.isnum[i]:
                    line[i] = int(line[i])
            self.testSet.append(line)
            line = fo.readline()

    def training(self):
        '''
        Get mean and var
        :return:NONE
        '''
        for i in range(2):
            subdata = list()
            for _ in self.dataSet:
                if _[-1] == i:
                    subdata.append(_)
                    self.sexSize[i] += 1
            self.mean.append(self.getMean(subdata))
            self.var.append(self.getVar(subdata))

    def Gauss(self, u, v, x):
        return math.exp(-(x - u) ** 2 / (2 * v)) / math.sqrt(2 * math.pi * v)

    def Classifier(self):
        '''
        :param sample: list[vector] Test sample
        :return: list[_index] Classifier result
        '''
        res = list()
        for samplex in self.testSet:
            _Psex = [self.sexSize[0], self.sexSize[1]]
            Psex = list(_Psex)

            for sex in range(2):
                for i in range(0, self.vectorLength):
                    if self.isnum[i]:
                        Psex[sex] *= self.Gauss(self.mean[sex][i], self.var[sex][i], samplex[i])
                    else:
                        Psex[sex] *= self.mean[sex][i][samplex[i]] ** 2 / self.sexSize[sex]
            # Psex = [Psex[0] / (Psex[0] + Psex[1]), Psex[1] / (Psex[0] + Psex[1])]

            res.append(Psex.index(max(Psex)))
        return res


nb = naive_bayes()
res = nb.Classifier()
ans = ''
for r in res:
    ans = ans + str(r)
print ans
