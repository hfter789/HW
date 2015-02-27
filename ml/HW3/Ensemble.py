from sklearn import tree
from math import * 
import string
import random
import numpy

# X = [[0, 0], [1, 1],[1,0],[0,1]]
# X = [[0, 0,1], [1, 1,0],[1,0,0],[0,1,1], [2, 1,0],[1,0,3],[0,6,1]]
# Y = [0, 1,0,1,0, 1,0]
# clf = tree.DecisionTreeClassifier(criterion='entropy',max_depth = 1)
# clf = clf.fit(X, Y)
# dot_data = StringIO() 
# tree.export_graphviz(clf, out_file=dot_data) 
# graph = pydot.graph_from_dot_data(dot_data.getvalue()) 
# graph.write_pdf("iris.pdf") 

def ParseFile(name):
	content = None
	with open(name) as f:
		content = f.readlines()

	if content == None:
		print "Wrong Content"
	X = []
	Y = []
	for line in content:
		# print ">>", line
		tokens = string.split(line)
		# print ">>", tokens[0], ">>", tokens[1]
		s = tokens[0]
		sample = []
		for i in range(len(s)):
			c = s[i]
			if c == 'a':
				sample.append(0)
			elif c == 't':
				sample.append(1)
			elif c == 'c':
				sample.append(2)
			elif c == 'g':
				sample.append(3)
			else:
				print 'Having something other than "atcg" at Iteration:',i, c
				break
		X.append(sample)
		s = tokens[1][0]
		if s == '+':
			Y.append(1)
		elif s == '-':
			Y.append(0)
		else:
			print 'Result should only be "+/-" but have',s
			continue

	return X,Y

def Bagging(X_train,Y_train,X_test, Y_test, sampleSize, Iteration = 50, depth = 1):
	N = len(X_train)
	# classifiers = []
	#recording the prediction instead of the classifier since we only need to predict test data
	predictions = numpy.array([0]*len(Y_test))
	for i in range(Iteration):
		X_Sample = []
		Y_Sample = []
		for j in range(sampleSize):
			k = random.randint(0,N-1)
			X_Sample.append(X_train[k])
			Y_Sample.append(Y_train[k])
		clf = tree.DecisionTreeClassifier(criterion = 'entropy', max_depth = depth)
		clf = clf.fit(X_Sample, Y_Sample)
		# classifiers.append(clf)
		#Now do the prediction with clf
		Y_Predict = clf.predict(X_test)
		#summing up the votes since the old votes stay the same
		#no need to do the calculation everytime
		predictions +=Y_Predict
		errorCount = 0
		for j in range(len(Y_test)):
			vote = predictions[j]/float(i+1)
			pred = 1 if vote > 0.5 else 0
			if pred != Y_test[j]:
				errorCount += 1
		print float(errorCount)/len(Y_test) 

def AdaBoost(X_train,Y_train,X_test,Y_test,Iteration = 50, depth = 1):
	N = len(X_train)
	predictions = numpy.array([0]*len(Y_test))
	trainingPred = numpy.array([0]*len(Y_train))
	#initialize data weight D
	D = numpy.array([float(1)/N]*N)
	# for i in range(Iteration):
	for i in range(Iteration):
		#train data
		clf = tree.DecisionTreeClassifier(criterion = 'entropy', max_depth = depth)
		clf = clf.fit(X_train,Y_train,sample_weight=D)
		#calculate error
		pred = clf.predict(X_train)
		error = 0.0
		for j in range(N):
			if pred[j] != Y_train[j]:
				error += D[j]
		alpha = log((1-error)/error)/2
		#update weight
		for j in range(N):
			D[j] =D[j] * exp(-alpha*Y_train[j]*pred[j])

		#normalize
		s = sum(D)
		for j in range(N):
			D[j] = D[j] / s
		#now make a prediction base on data
		#==================================TRAIN==============================#
		pred = clf.predict(X_train)
		trainingPred = trainingPred + pred * alpha
		trainErrorCount = 0
		#check error
		for j in range(N):
			p = -1
			if trainingPred[j] > 0:
				p = 1
			if p != Y_train[j]:
				trainErrorCount+=1
		#==================================TEST==============================#
		pred = clf.predict(X_test)
		predictions = predictions + pred * alpha
		errorCount = 0
		#check error
		for j in range(len(Y_test)):
			p = -1
			if predictions[j] > 0:
				p = 1
			if p != Y_test[j]:
				errorCount+=1
		print float(trainErrorCount) / N , ",", float(errorCount) / len(Y_test),",", float(trainErrorCount)/N - float(errorCount)/len(Y_test)
		# print float(errorCount) / len(Y_test)

#M is the sample size
#N is the range
#In English, sample M items from N items with replacement
def sampleExperiment(M,N,Iteration = 50):
	for i in range(Iteration):
		a = set()
		for j in range(M):
			k = random.randint(0,N-1)
			a.add(k)
		print len(a)/float(N)

def main():
	X_train,Y_train = ParseFile('training.txt')
	X_test,Y_test = ParseFile('test.txt')
	# Bagging(X_train,Y_train, X_test, Y_test,60,Iteration = 100)
	# Bagging(X_train,Y_train, X_test, Y_test,60,Iteration = 100,depth = 2)
	# sampleExperiment(len(X_train),len(X_train),Iteration = 100)

	for i in range(len(Y_train)):
		if Y_train[i] == 0:
			Y_train[i] = -1

	for i in range(len(Y_test)):
		if Y_test[i] == 0:
			Y_test[i] = -1 
	AdaBoost(X_train,Y_train,X_test,Y_test,Iteration = 200,depth = 2)


if __name__ == '__main__':
	main()
	# pass