from numpy import *
import operator

def textMatrix(filename):
	arrayLines = open(filename).readlines()
	numberOfLines = len(arrayLines)
	returnMat = zeros((numberOfLines, 3))
	classLabel = []
	index = 0
	for line in arrayLines:
		line = line.strip()
		listFromline = line.split('\t')
		returnMat[index,] = listFromline[0:3]
		classLabel.append(int(listFromline[-1]))
		index+=1
	return returnMat, classLabel

def autoNorm(dataSet):
	minNum = dataSet.min(0)
	maxNum = dataSet.max(0)
	arrange = maxNum - minNum
	m = dataSet.shape[0]
	minMat = tile(minNum,(m, 1))
	arrangeMat = tile(arrange,(m, 1))
	normData = (dataSet-minMat)/arrangeMat
	return normData, arrange, minNum


def classify(inX, dataSet, labels, k):
	dataSetSize = dataSet.shape[0]
	diffMat = tile(inX, (dataSetSize,1)) - dataSet
	sqdiffMat = diffMat**2
	sqDistances = sqdiffMat.sum(axis=1)
	Distances = sqDistances**0.5
	index = Distances.argsort()
	classCounts = {}
	for i in range(k):
		votelabels = labels[index[i]]
		classCounts[votelabels] = classCounts.get(votelabels, 0) + 1
	sortClass = sorted(classCounts.iteritems(), key = operator.itemgetter(1), reverse = True)
	return sortClass[0][0]



def datingClass():
	Ratio = 0.10
	datingDataMat, labels = textMatrix('datingTestSet.txt')
	normMat, ranges, minNum = autoNorm(datingDataMat)
	m = normMat.shape[0]
	testNum = int(m*Ratio)
	errorCount = 0.0
	for i in range(testNum):
		classResult = classify(normMat[i,:], normMat[testNum:m,:], labels[testNum:m], 20)
		print 'the class came back is :%d , the real answer is : %d' %(classResult, labels[i])
		if classResult != labels[i]:
			errorCount+=1.0
	print 'the error rate is : %f'  %(errorCount/float(testNum))

datingClass()
