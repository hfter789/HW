from sklearn import tree
from sklearn.externals.six import StringIO  
import string
import pydot 
import random

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

def Bagging(X_train,Y_train,X_test, Y_test, sampleSize, Iteration = 50, depth = 1, printError = True):
	N = len(X_train)
	# classifiers = []
	#recording the prediction instead of the classifier since we only need to predict test data
	predictions = [0] * len(Y_test)
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
		predictions +=Y_Predict
		M = len(predictions)
		errorCount = 0
		for j in range(len(Y_test)):
			if Y_Predict[j] != Y_test[j]:
				errorCount += 1
		print float(errorCount)/len(Y_test) 

	return classifiers

def main():
	X_train,Y_train = ParseFile('training.txt')
	X_test,Y_test = ParseFile('test.txt')
	Bagging(X_train,Y_train, X_test, Y_test,sampleSize = 60, Iteration = 100)

if __name__ == '__main__':
	main()
	# pass