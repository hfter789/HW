import numpy
import scipy.sparse as sp
import scipy.sparse.linalg as spla
from scipy.sparse import vstack, hstack
from math import sqrt

def calcRMSE(prediction,result):
	RMSE = sqrt(sum((prediction - result)**2)/len(prediction))
	# print RMSE
	return RMSE

y = numpy.loadtxt("upvote_labels.txt", dtype=numpy.int)
featureNames = open("upvote_features_100.txt").read().splitlines()
A=sp.csc_matrix(numpy.genfromtxt("upvote_data_100.csv",delimiter=","))


testData = A[5000:]
testResult = y[5000:]

#add a column to the training data

indptr = range(101)
indices = [0]*100
data = [1] * 100

addon = sp.csc_matrix( (data,indices,indptr), shape=(1,100), dtype=float)
trainingData = A[:5000]
trainingData = vstack([trainingData,addon])

trainingResult = y[:5000]
trainingResult = numpy.append(trainingResult,[1])

Ht = trainingData.transpose(True)
a = Ht * trainingData
t = Ht * trainingResult
Ainv = spla.inv(a)

w = Ainv * t

prediction = trainingData * w

print "Part 1 Training RMSE: ", calcRMSE(prediction,trainingResult)

prediction = testData * w
# diff = prediction - testResult
# diff = [n**2 for n in diff]

print "Part 1 Testing RMSE: ", calcRMSE(prediction,testResult)

###############################Part 2 ##################################

trainingData = A[:5000]
trainingResult = y[:5000]

lamda = 1.0
folding = 5
folds = {}
foldsResult = {}
#split the data
for i in range(folding):
	folds[i] = trainingData[(i*1000):((i+1)*1000)]
	foldsResult[i] = trainingResult[(i*1000):((i+1)*1000)]

#assemble the data
iden = sp.identity(99)

indptr = range(100)
indices = [0]*99
data = [0] * 99

addon = sp.csc_matrix( (data,indices,indptr), shape=(1,99), dtype=float)
iden = vstack([addon,iden])
indptr = [0,1]
indices = range(100)
data = [0] * 100

addon = sp.csc_matrix( (data,indices,indptr), shape=(100,1), dtype=float)
iden = hstack([addon,iden])

for i in range(folding):
	print "#############################Using ", i, "th folds#################################"
	tuningData = folds[i]
	tuningResult = foldsResult[i]
	H = t = None
	for j in range(folding):
		if(j != i):
			if(H is None):
				H = folds[j]
				t = foldsResult[j]
			else:	
				H = vstack([H,folds[j]])
				t = numpy.concatenate((t,foldsResult[j]))
	#calculate w
	lamda = 1.0
	factor = 0.75
	for i in range(20):
		# print "Using lamda = ", lamda
		print lamda
		w = spla.inv(H.transpose()*H + lamda * iden) * H.transpose() * t
		trainingPred = trainingData * w
		valid = tuningData * w
		print calcRMSE(trainingPred,trainingResult)
		# print "Training RMSE ", calcRMSE(trainingPred,trainingResult)
		# print "Validation RMSE ", calcRMSE(valid,tuningResult)
		lamda*= factor


