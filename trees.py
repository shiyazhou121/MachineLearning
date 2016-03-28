from math import log
import operator



def ShannonEnt(dataSet):
	numEntries = len(dataSet)
	classlabels = {}
	for each in dataSet:
		currentlabel = each[-1]
		classlabels[currentlabel] = classlabels.get(currentlabel, 0) + 1
	shannonEnt = 0.0
	for each in classlabels:
		currentProb = float(classlabels[each])/int(numEntries)
		shannonEnt -= currentProb*log(currentProb, 2)
	return shannonEnt


def createDataSet():
	dataSet = [[1,1, 'yes'],
			   [1,1, 'yes'],
			   [1,0, 'no'],
			   [0,1, 'no'],
			   [0,1, 'no']]
	labels = ['no surfacing', 'flippers']
	return dataSet, labels


def splitDataSet(dataSet, axis, value):
	retDataSet = []
	for each in dataSet:
		if each[axis] == value:
			aferlist = each[:axis]
			aferlist.extend(each[axis+1:])
			retDataSet.append(aferlist)
	return retDataSet



def chooseBestFeatureToSplit(dataSet):
	numFeature = len(dataSet[0])-1
	myDat, labels = createDataSet()
	baseEntropy = ShannonEnt(myDat)
	bestInfoGain = 0.0
	bestFeature = -1
	for i in range(numFeature):
		featlist = [each[i] for each in dataSet]
		uniqueVals = set(featlist)
		newEntropy = 0.0
		for value in uniqueVals:
			subDataSet = splitDataSet(dataSet, i, value)
			prob = len(subDataSet)/float(len(dataSet))
			newEntropy += prob*ShannonEnt(subDataSet)
		infoGain = baseEntropy - newEntropy
		if(infoGain > bestInfoGain):
			bestInfoGain = infoGain
			bestFeature = i
	return bestFeature


def majorityCnt(classList):
	classCount = {}
	for each in classList:
		classCount[each] = classCount.get(each, 0) + 1
	sortedCount = sorted(classCount.iteritems(), key=operator.itemgetter(1), reverse=True)
	return sortedCount[0][0]


def createTree(dataSet, labels):
	classList = [each[-1] for each in dataSet]
	if classList.count(classList[0]) == len(classList):
		return classList[0]
	if len(dataSet[0]) == 1:
		return majorityCnt(classList)

	bestFeat = chooseBestFeatureToSplit(dataSet)
	bestFeatLabel = labels[bestFeat]

	myTree = {bestFeatLabel:{}}
	del(labels[bestFeat])
	featValues = [each[bestFeat] for each in dataSet]
	uniqueVals = set(featValues)

	for value in uniqueVals:
		subLabels = labels[:]
		myTree[bestFeatLabel][value] = createTree(splitDataSet(dataSet, bestFeat, value), subLabels)
	return myTree 



def classfiy(inputTree, featLabels, testVec):
	firstStr = inputTree.keys()[0]
	secondDict = inputTree[firstStr] 
	featIndex = featLabels.index(firstStr)
	for key in secondDict.keys():
		if testVec[featIndex] ==key:
			if type(secondDict[key]).__name__=='dict':
				classLabel = classfiy(secondDict[key], featLabels, testVec)
			else:
				classLabel = secondDict[key]
	print classLabel


myDat, labels = createDataSet()
testlabel = labels[:]
retrieveTree = createTree(myDat, labels)
print retrieveTree
print testlabel
classfiy(retrieveTree, testlabel, [1,0])
classfiy(retrieveTree, testlabel, [1,1])