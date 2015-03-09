import numpy
import random
from math import *
from sklearn.cluster import KMeans

def KMean(X,Y,K,Iterations=20,randomStart = False):
	#randomly pick K points
	dimension = len(X[0])
	centers = []
	if randomStart:
		centers = random.sample(X,K)
	oldGroups = {}
	groups = {}
	#use the first K points in X as centers
	for i in range(K):
		if(not randomStart):
			centers.append(X[i].copy())
		oldGroups[i] = []
		groups[i] = []
	#maps cluster index to array of data indices

	for i in range(Iterations):
		for j in range(len(X)):
			minDist = e**100
			minIndex = -1
			for k in range(K):
			#STEP 1 : group the data according to min distance
				dist = numpy.linalg.norm(X[j]-centers[k])
				if dist < minDist:
					minDist = dist
					minIndex = k
			groups[minIndex].append(j)
		#check convergence
		if groups == oldGroups:
			print "Converged at Iteration", i
			# print groups
			break
		oldGroups = groups

		#STEP 2 : recalc mean
		for k in range(K):
			sum = numpy.array([0] * dimension)
			for j in groups[k]:
				sum += X[j]
			centers[k] = sum/float(len(groups[k]))
		
		#clean the group
		groups = {}
		for k in range(K):
			groups[k] = []
	# if K != 10:
	# 	return
	#calc Sum of square
	for k in range(K):
		ss = 0
		for j in oldGroups[k]:
			ss += numpy.linalg.norm(X[j]-centers[k])**2
		print "Sum of square for cluster", k, ss
	#use oldGroup to to calculate mistake rate
	for k in range(K):
		count = [0] * 10
		data = oldGroups[k]
		for d in data:
			count[Y[d]] += 1
		maxCount = 0
		predIndex = -1
		for i in range(10):
			if count[i] > maxCount:
				maxCount = count[i]
				predIndex = i
		print "Cluster", k, "Prediction digit is", predIndex, "with accuracy", maxCount/float(len(data))


if __name__ == '__main__':
	X=numpy.genfromtxt('digit.txt')
	Y=numpy.genfromtxt('labels.txt',dtype=int)
	# X = numpy.array([[-1,0],[0,0],[2,2]])
	# KMean(X,Y,2)
	# KMean(X,Y,4)
	KMean(X,Y,6)
	# KMean(X,Y,10,randomStart=True)
	# cluster = KMeans(n_clusters=6,max_iter=20)
	# cluster = cluster.fit(X)
	# print cluster.score(X)