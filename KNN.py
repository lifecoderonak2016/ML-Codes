# Ronak Kumar (2015080)

import csv
import math
import random
import sys
import operator

def loadData(filename, split, trainingSet = [], testSet = []):
	with open(filename, 'rb') as csvfile:
		lines = csv.reader(csvfile)
		dataset = list(lines)
		for x in range(len(dataset) - 1):
			for y in range(4):
				dataset[x][y] = float(dataset[x][y])
			if random.random() < split:
				trainingSet.append(dataset[x])
			else:
				testSet.append(dataset[x])

def distance(value1, value2, length):
	dist = 0
	for x in range(length):
		dist += pow((value1[x] - value2[x]), 2)
	return math.sqrt(dist)

def getDistance(x, y, z):
	distance(x, y, z)

def getNeighbours(trainingSet, testValue, size):
	distances = []
	length = len(testValue) - 1
	for x in range(len(trainingSet)):
		distValue = getDistance(testValue, trainingSet[x], length)
		distances.append((trainingSet[x], distValue))
	distances.sort(key = operator.itemgetter(1))
	neighbours = []
	for x in range(size):
		neighbours.append(distances[x][0])
	return neighbours

def getFeedback(neighbours):
	classVotes = {}
	for x in range(len(neighbours)):
		feedback = neighbours[x][-1]
		if(feedback in classVotes):
			classVotes[feedback] += 1
		else:
			classVotes[feedback] = 1
	votes = sorted(classVotes.iteritems(), key = operator.itemgetter(1), reverse = True)
	return votes[0][0]	

def accuracy(testSet, predictions):
	flag = 0
	for x in range(len(testSet)):
		if(testSet[x][-1] == predictions[x]):
			flag += 1
		return (flag / float(len(testSet))) * 100.0

def main():
	trainingSet = []
	testSet = []
	splitRatio = 0.7;
	# Add the name of the .csv file
	# loadData('test.data', splitRatio, trainingSet, testSet)
	loadData('file.data', splitRatio, trainingSet, testSet)
	print 'Length of Training Set is ' + repr(len(trainingSet))
	print 'Length of Test Set is ' + repr(len(testSet))
	predictions = []
	value = 3
	for x in range(len(testSet)):
		neighbours = getNeighbours(trainingSet, testSet[x], value)
		result = getFeedback(neighbours)
		predictions.append(result)
		print 'Predicted Value ' + repr(result) + ' Actual Result ' + repr(testSet[x][-1])
	acc = accuracy(testSet, predictions)
	print 'Accuracy of Prediction is ' + repr(acc)		

if __name__ == '__main__':
	main()
