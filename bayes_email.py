from numpy import *
import random


def loadDataSet():
	postingList = [ ['my','dog','has','flea','problems','help','please'],
					['maybe','not','take','him','to','dog','park','stupid'],
					['my','dalmation','is','so','cute','i','love','her'],
					['stop','posting','stupid','worthless','garbage'],
					['mr','licks','ate','my','steak','how','to','stop','him'],
					['quit','buying','worthless','dog','food','stupid']]
	classVec = [0,1,0,1,0,1]

	return postingList, classVec

def createVocabList(dataSet):
	vocabSet = set([])
	for document in dataSet:
		vocabSet = vocabSet | set(document)
	return list(vocabSet)

def setOfWords2Vec(vocabList, inputSet):
	returnVec = [0]*len(vocabList)
	for word in inputSet:
		if word in vocabList:
			returnVec[vocabList.index(word)] = 1
		else:
			print "the word: %s is not in my Vocabulary!"  %word
	return returnVec

def createdVecOfwords(vocabList, inputSet):
	returnList = []
	for i in range(len(inputSet)):
		returnList.append(setOfWords2Vec(vocabList, inputSet[i]))
	return returnList

def trainNB(trainMatrix, trainCategory):
	numTrainDocs = len(trainMatrix)
	numWords = len(trainMatrix[0])
	pAbusive = sum(trainCategory)/float(numTrainDocs)
	p0Num = ones(numWords)
	p1Num = ones(numWords)
	p0Denom = 2.0
	p1Denom = 2.0
	for i in range(numTrainDocs):
		if trainCategory[i] == 1:
			p1Num += trainMatrix[i]
			p1Denom += sum(trainMatrix[i])
		else:
			p0Num += trainMatrix[i]
			p0Denom += sum(trainMatrix[i])
	p0Vect = log(p0Num/p0Denom)
	p1Vect = log(p1Num/p1Denom)
	return p0Vect, p1Vect, pAbusive


def classifyNB(vec,vocab, p0Vec, p1Vec, classVec):
	thisDoc = array(setOfWords2Vec(vocab, vec))
	p0 = sum(thisDoc*p0Vec)+log(1.0 - classVec)
	p1 = sum(thisDoc*p1Vec)+log(classVec)
	if p0>p1:
		return 0
	else:
		return 1


def textParse(bigstring):
	import re
	listOfTokens = re.split(r'\w*', bigstring)
	return [each.lower() for each in bigstring if len(each) > 2]


def spamTest():
	docList = []
	classList = []
	fullText = []
	for i in range(1, 26):
		wordList = textParse(open('email/spam/%d.txt' %i).read())
		docList.append(wordList)
		fullText.extend(wordList)
		classList.append(1)
		wordList = textParse(open('email/ham/%d.txt' %i).read())
		docList.append(wordList)
		fullText.extend(wordList)
		classList.append(0)
	vocabList = createVocabList(docList)
	trainSet = range(50)
	testSet = []
	for i in range(10):
		randIndex = int(random.uniform(0,len(trainSet)))
		testSet.append(trainSet[randIndex])
		del(trainSet[randIndex])
	trainMat = []
	trainclass = []
	for docIndex in trainSet:
		trainMat.append(setOfWords2Vec(vocabList, docList[docIndex]))
		trainclass.append(docList[docIndex])
	p0V, p1V, pSpam = trainNB(array(trainMat), array(trainclass))
	errorCount = 0.0
	for docIndex in testSet:
		wordVector = setOfWords2Vec(vocabList, docList[docIndex])
		result = classifyNB(array(wordVector), vocabList, p0V, p1V, pSpam)
		if result != classList[docIndex]:
			errorCount += 1
	print 'the error rate is : %f'  %(float(errorCount)/len(testSet))
	return float(errorCount)/len(testSet)


sumCount = 0.0
for i in range(5):
	sumCount += spamTest()

print sumCount/5