#!/usr/bin/python
from __future__ import division
from numpy import *
from math import *
import time

def calcWeight(ng, lamda, Y_train, X_train, dimension, iteration = 1):

	weight = zeros((dimension,1),dtype=float)
	# figure out weight[0]
	for y in Y_train:
		weight[0] += ng * (y - 1/2)
	weight[0] = weight[0]/len(X_train)

	for i in range(iteration):

		for j in range(1,dimension):
			# v is the sum of xj(yj - P(Yj=1|xj,w))
			v = 0
			for k in range(len(X_train)):
				#don't dot with weight 0
				# start = time.time()
				s = weight[0] + weight[1:].T.dot(X_train[k])
				# end = time.time()
				# print end - start
				try:
					# start = time.time()
					v += X_train[k][j-1] * (Y_train[k] - exp(s)/(1+exp(s)))
					# end = time.time()
					# print end - start
				except:
					print s
				# print "s is", s
				# print "v is", v

			weight[j] += ng * (-lamda*weight[j]+v/len(X_train))
			# print "Weight at", j, " is", weight[j]

	print weight
	return weight

def main():
	training_data = genfromtxt('train.txt', delimiter=',')
	Y_train = training_data[:,0]
	X_train = training_data[:, 1:]
	Y_test = genfromtxt('test_label.txt', delimiter=',')
	X_test = genfromtxt('test.txt', delimiter=',')

	ng = 0.1
	lamda = 0.3
	weight = calcWeight(ng,lamda,Y_train,X_train,55)
	count = 0
	for i in range(len(Y_test)):
		prediction = weight[1:].T.dot(X_test[i])
		if prediction > 0:
			prediction = 1
		else:
			prediction = 0
		if prediction == Y_test[i]:
			count += 1
	print float(count) / len(Y_test)
if __name__ == '__main__':
	main()
