import numpy
import scipy.sparse as sp
import scipy.sparse.linalg as spla
from scipy.sparse import vstack, hstack
from math import sqrt
def calcRMSE(prediction,result):
	RMSE = sqrt(sum((prediction - result)**2)/len(prediction))
	# print RMSE
	return RMSE

def crossVald(folding):
	trainingData = A[:5000]
	trainingResult = y[:5000]

	testData = A[5000:]
	testResult = y[5000:]
	mul = len(trainingResult)/folding

	#add a column to the test data
	row = range(1000)
	col = [0] * 1000
	data = [1] * 1000

	addon = sp.csc_matrix( (data,(row,col)), shape=(1000,1), dtype=float)
	testData = hstack([addon, testData])


	folds = {}
	foldsResult = {}
	#split the data
	for i in range(folding):
		folds[i] = trainingData[(i*mul):((i+1)*mul)]
		foldsResult[i] = trainingResult[(i*mul):((i+1)*mul)]

	row = range(5000)
	col = [0] * 5000
	data = [1] * 5000

	addon = sp.csc_matrix( (data,(row,col)), shape=(5000,1), dtype=float)
	trainingData = A[:5000]
	trainingData = hstack([addon, trainingData])

	#assemble the data
	iden = sp.identity(100)

	indptr = range(101)
	indices = [0]*100
	data = [0] * 100

	addon = sp.csc_matrix( (data,indices,indptr), shape=(1,100), dtype=float)
	iden = vstack([addon,iden])
	indptr = [0,1]
	indices = range(101)
	data = [0] * 101

	addon = sp.csc_matrix( (data,indices,indptr), shape=(101,1), dtype=float)
	iden = hstack([addon,iden])
	l = {}
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
		#add a columb 4000 * 1
		row = range(5000 - mul)
		col = [0] * (5000 - mul)
		data = [1] * (5000 - mul)

		addon = sp.csc_matrix( (data,(row,col)), shape=((5000-mul),1), dtype=float)
		H = hstack([addon, H])
		
		row = range(mul)
		col = [0] * mul
		data = [1] * mul

		addon = sp.csc_matrix( (data,(row,col)), shape=(mul,1), dtype=float)
		tuningData = hstack([addon, tuningData])
		#calculate w
		lamda = 1.0
		factor = 0.75
		#decrease lambda by 25% each time for 20 times
		for i in range(20):
			# print "Using lamda = ", lamda
			# print lamda
			w = spla.inv(H.transpose()*H + lamda * iden) * H.transpose() * t
			trainingPred = trainingData * w
			valid = tuningData * w
			if lamda in l:
				l[lamda] += calcRMSE(valid,tuningResult)
			else:
				l[lamda] = calcRMSE(valid,tuningResult)

			print  calcRMSE(trainingPred,trainingResult)
			# print "Training RMSE ", calcRMSE(trainingPred,trainingResult)
			# print "Validation RMSE ", calcRMSE(valid,tuningResult)
			lamda*= factor

	#find lambda that generates minimum RMSE in the tuning data
	minRMSE = 1000
	minL = 0
	for x in l:
		if l[x] < minRMSE:
			minRMSE = l[x]
			minL = x
	print minL, minRMSE
	w = spla.inv(trainingData.transpose()*trainingData + minL * iden) * trainingData.transpose() * trainingResult
	testPred = testData * w
	print "Testing RMSE is",calcRMSE(testPred,testResult)

y = numpy.loadtxt("upvote_labels.txt", dtype=numpy.int)
featureNames = open("upvote_features_100.txt").read().splitlines()
A=sp.csc_matrix(numpy.genfromtxt("upvote_data_100.csv",delimiter=","))


testData = A[5000:]
testResult = y[5000:]

#add a column to the training data

row = range(5000)
col = [0] * 5000
data = [1] * 5000

addon = sp.csc_matrix( (data,(row,col)), shape=(5000,1), dtype=float)
trainingData = A[:5000]
trainingData = hstack([addon, trainingData])

trainingResult = y[:5000]
# trainingResult = numpy.append(trainingResult,[1])
#add a column to the test data
row = range(1000)
col = [0] * 1000
data = [1] * 1000

addon = sp.csc_matrix( (data,(row,col)), shape=(1000,1), dtype=float)
testData = hstack([addon, testData])

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

crossVald(5)
# crossVald(10)


