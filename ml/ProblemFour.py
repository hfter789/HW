import numpy
import scipy.sparse as sp
import scipy.sparse.linalg as spla
from scipy.sparse import vstack
from math import sqrt

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
A = Ht * trainingData
t = Ht * trainingResult
Ainv = spla.inv(A)

w = Ainv * t

prediction = trainingData * w

RMSE = sqrt(sum((prediction - trainingResult)**2)/len(prediction))
print RMSE

prediction = testData * w
# diff = prediction - testResult
# diff = [n**2 for n in diff]

RMSE = sqrt(sum((prediction - testResult)**2)/len(prediction))
print RMSE

lamda = 1.0
folding = 5

for i in range(folding):
	d = trainingData[0:i*1000]+trainingData[(i+1) * 1000:]
	t = trainingData[i*1000:(i+1)*1000]
	print len(d)
	print len(t)


