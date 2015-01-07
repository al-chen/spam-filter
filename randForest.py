import csv
import numpy as np
import math
from random import randint, sample
from collections import Counter

class Tree(object):
	def __init__(self, left=None, right=None, feature=None, threshold=None, label=None):
		self.left = left
		self.right = right
		self.feature = feature
		self.threshold = threshold
		self.label = label
	def toString(self):
		if self.label != None:
			return "Label: " + str(self.label) + " "
		return "Feature: " + str(self.feature) + " Threshold: " + str(self.threshold) + " " + self.left.toString() + " " + self.right.toString() + " "

with open('trainLabels.csv', 'rb') as csvTrainLabels:
	trainLabels = csv.reader(csvTrainLabels, delimiter=',')
	labels = []
	for row in trainLabels:
		labels.append(int(row[0]))
	# print labels

# with open('trainFeatures.csv', 'rb') as csvTrainFeatures:
# 	trainFeatures = csv.reader(csvTrainFeatures, delimiter=',')
# 	i = 0
# 	dic = {}
# 	for row in trainFeatures:
# 		dic[tuple(row)] = labels[i]
# 		i += 1

with open('trainFeatures.csv', 'rb') as csvTrainFeatures:
	trainFeatures = csv.reader(csvTrainFeatures, delimiter=',')
	S = []
	dic = {}
	i = 0
	for trainRow in trainFeatures:
		temp = tuple(map(float, trainRow))
		S.append(temp)
		dic[temp] = labels[i]
		i += 1

def bag(lst):
	l = len(lst)
	newList = []
	for i in range(l):
		r = randint(0,l-1)
		newList.append(lst[r])
	return list(set(newList))

def entropy(lst):
	count1 = 0
	count0 = 0
	for row in lst:
		if dic[row] == 1:
			count1 += 1
		else:
			count0 += 1
	l = len(lst)
	if count1 == 0 or count0 == 0 or l == 0:
		return 0.0
	return -(float(count1)/l * math.log(float(count1)/l,2)) - (float(count0)/l * math.log(float(count0)/l,2))

def majority(lst):
	list_of_classes = []
	for entry in lst:
		list_of_classes.append(dic[entry])
	c = Counter(list_of_classes)
	print c.most_common(1)
	label = c.most_common(1)[0][0]
	return label

def buildDecTree(lst, level=0):
	# print "Level " + str(level)
	Sbag = bag(lst)
	if Sbag == []:
		print "----------hello----------"
		return Tree(None, None, None, None, 0)
	first_class = dic[Sbag[0]]
	# print(Sbag)
	# print first_class
	boo = True
	list_of_classes = []
	for entry in Sbag:
		list_of_classes.append(dic[entry])
		if dic[entry] != first_class:
			boo = False
	if boo or level >= 15: # stopping conditions: Label leaf with class that appears most frequently in Sbag. Return tree.
		# print len(list_of_classes)
		c = Counter(list_of_classes)
		label = c.most_common(1)[0][0]
		# print label
		# print c.most_common(1)
		return Tree(None, None, None, None, label)
	features = [i for i in range(0,57)]
	features = sorted(sample(features, 8))
	# print features
	Y = entropy(Sbag)
	best_goodness = 0.0
	best_sl = []
	best_sr = []
	best_feature = -1
	best_threshold = 0.0
	for feature in features:
		values_of_feature = []
		for entry in Sbag:
			value = entry[feature]
			if value in values_of_feature:
				continue
			values_of_feature.append(value)
		values_of_feature = sorted(values_of_feature)
		# print values_of_feature
		if len(values_of_feature) == 1:
			possible_threshold = values_of_feature[0]
			sl = []
			sr = []
			for entry in Sbag:
				sl.append(entry)
			yl = entropy(sl)
			goodness = Y - yl
			if float(goodness) >= float(best_goodness):
				# print "GOODNESS: " + str(goodness)
				best_goodness = goodness
				best_sl = sl
				best_sr = sr
				best_feature = feature
				best_threshold = possible_threshold
		else:
			for i in range(1, len(values_of_feature)):
				possible_threshold = (float(values_of_feature[i-1]) + float(values_of_feature[i])) / float(2)
				sl = []
				sr = []
				for entry in Sbag:
					if entry[feature] <= possible_threshold:
						sl.append(entry)
					else:
						sr.append(entry)
				yl = entropy(sl)
				yr = entropy(sr)
				goodness = Y - ((float(len(sl)) / float(len(Sbag)) * yl) + (float(len(sr)) / float(len(Sbag)) * yr))
				if float(goodness) >= float(best_goodness):
					# print "GOODNESS: " + str(goodness)
					best_goodness = goodness
					best_sl = sl
					best_sr = sr
					best_feature = feature
					best_threshold = possible_threshold

	
	if best_sl == []:
		return Tree(buildDecTree(best_sr, level+1), buildDecTree(best_sr, level+1), best_feature, best_threshold, None)
	elif best_sr == []:
		return Tree(buildDecTree(best_sl, level+1), buildDecTree(best_sl, level+1), best_feature, best_threshold, None)
	return Tree(buildDecTree(best_sl, level+1), buildDecTree(best_sr, level+1), best_feature, best_threshold, None)

T = 25
decTrees = []
for i in range(T):
	print("Tree " + str(i+1))
	decTrees.append(buildDecTree(S))


with open('emailOutput1.csv', 'wb') as csv1:
	writer1 = csv.writer(csv1, delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)
	with open('emailOutput2.csv', 'wb') as csv2:
		writer2 = csv.writer(csv2, delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)
		with open('emailOutput5.csv', 'wb') as csv5:
			writer5 = csv.writer(csv5, delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)
			with open('emailOutput10.csv', 'wb') as csv10:
				writer10 = csv.writer(csv10, delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)
				with open('emailOutput25.csv', 'wb') as csv25:
					writer25 = csv.writer(csv25, delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)
					with open('valFeatures.csv', 'rb') as csvVal:
						valFeatures = csv.reader(csvVal, delimiter=',')
						for valRow in valFeatures:
							votes = []
							forest = decTrees[:]
							for tree in forest:
								while True:
									if tree.label != None:
										votes.append(tree.label)
										break
									else:
										if float(valRow[tree.feature]) <= float(tree.threshold):
											tree = tree.left
										else:
											tree = tree.right
							# T=1
							guess = votes[0]
							writer1.writerow([guess])

							# T=2
							votes2 = votes[:2]
							guess = max(set(votes2), key=votes2.count)
							writer2.writerow([guess])

							# T=5
							votes5 = votes[:5]
							guess = max(set(votes5), key=votes5.count)
							writer5.writerow([guess])

							# T=10
							votes10 = votes[:10]
							guess = max(set(votes10), key=votes10.count)
							writer10.writerow([guess])

							# T=25
							votes25 = votes
							guess = max(set(votes25), key=votes25.count)
							writer25.writerow([guess])

# with open('emailOutput.csv', 'wb') as csvTest:
# 	writerTest = csv.writer(csvTest, delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)				
# 	with open('testFeatures.csv', 'rb') as csvTestFeatures:
# 		testFeatures = csv.reader(csvTestFeatures, delimiter=',')
# 		for testRow in testFeatures:
# 			votes = []
# 			forest = decTrees[:]
# 			for tree in forest:
# 				while True:
# 					if tree.label != None:
# 						votes.append(tree.label)
# 						break
# 					else:
# 						if float(testRow[tree.feature]) <= float(tree.threshold):
# 							tree = tree.left
# 						else:
# 							tree = tree.right
# 			guess = max(set(votes), key=votes.count)
# 			print guess
# 			writerTest.writerow([guess])



# with open('emailOutput' + str(T) + '.csv', 'wb') as csvfile:
# with open('emailOutput.csv', 'wb') as csvfile:
# 	writer = csv.writer(csvfile, delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)
# 	with open('testFeatures.csv', 'rb') as csvVal:
# 		valFeatures = csv.reader(csvVal, delimiter=',')
# 		for valRow in valFeatures:
# 			votes = []
# 			for tree in forest:
# 				while True:
# 					if tree.label != None:
# 						# print(tree.label)
# 						votes.append(tree.label)
# 						break
# 					else:
# 						if float(valRow[tree.feature]) <= float(tree.threshold):
# 							tree = tree.left
# 						else:
# 							tree = tree.right
# 			guess = max(set(votes), key=votes.count)
# 			print guess
# 			writer.writerow([guess])