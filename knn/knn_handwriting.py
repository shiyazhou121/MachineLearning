from numpy import *
import operator
from os import listdir


def imgToVector(filename):
	needVector = zeros((1, 1024))
	fr = open(filename)
	for i in range(32):
		lineStr = fr.readline()
		for j in range(32):
			needVector[0,32*i+j] = int(lineStr[j])
	return needVector


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


def handWritingClass():
	trainingFileList = listdir('trainingDigits')
	m = len(trainingFileList)
	trainingMat = zeros((m, 1024))
	trainingLabels = []
	for i in range(m):
		fileNameStr = trainingFileList[i]
		filename = int(fileNameStr.split('_')[0])
		trainingLabels.append(filename)
		trainingMat[i,:] = imgToVector('trainingDigits/%s'%fileNameStr) 

	errorCount = 0.0
	testFileList = listdir('testDigits')
	mTest = len(testFileList)
	for i in range(mTest):
		testNameStr = testFileList[i]
		testlabels = int(testNameStr.split('_')[0])
		testInX = imgToVector('testDigits/%s' %testNameStr)
		returnTest = classify(testInX, trainingMat, trainingLabels, 20)
		print 'the test is : %s, the real is : %s' %(returnTest, testlabels)
		if returnTest!=testlabels:
			errorCount+=1
	print 'the total error is : %f' %errorCount
	print 'the error rate is : %f' %(errorCount/float(mTest))



handWritingClass()
