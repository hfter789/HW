#!/usr/bin/python
from __future__ import division
from numpy import *
from math import *
import pdb

def calcWeight(ng, lamda, Y_train, X_train, dimension, iteration = 1):

	weight = zeros((dimension,1),dtype=float)
	N = len(X_train)
	for i in range(iteration):
		# figure out weight[0]
		error = 0
		for j in range(N):
			s = weight.T.dot(X_train[j])
			error += Y_train[j] - exp(s)/(1+exp(s))
		#pdb.set_trace()
		weight[0] += error * ng / N

		#this gives the overall dot product
		val = dot(X_train.T ,(Y_train - dot(X_train,weight[1:].T)))/N
		weight[1:] += ng * (-lamda*weight[1:] + val)

		count = 0
		for i in range(len(Y_train)):
			s = weight.T.dot(X_train[i])
			prediction = exp(s)/(1+exp(s))
			res = 0
			if prediction > 0.5:
				res = 1
			if res == Y_train[i]:
				count += 1

			print "****P is",prediction, "and true result is", Y_train[i]
		#print count
		print "Training Acc is ", float(count) / len(Y_train)

	print weight
	return weight

def main():
	training_data = genfromtxt('train.txt', delimiter=',')
	Y_train = training_data[:,0]
	X_train = training_data[:, 1:]
	Y_test = genfromtxt('test_label.txt', delimiter=',')
	X_test = genfromtxt('test.txt', delimiter=',')
	#try not adding a column
	#add a column of 1 to the training data
	addon = array([1]*len(X_train)).reshape((len(X_train),1))
	X_train = hstack((addon, X_train))

	addon = array([1]*len(X_test)).reshape((len(X_test),1))
	X_test = hstack((addon, X_test))

	ng = 0.1
	lamda = 0.3
	weight = calcWeight(ng,lamda,Y_train,X_train,55,1000)

	count = 0
	for i in range(len(Y_train)):
		prediction = weight.T.dot(X_train[i])
		if prediction > 0:
			print "HIT"
			prediction = 1
		else:
			prediction = 0
		if prediction == Y_train[i]:
			count += 1
	print count
	print "Training Error is ", float(count) / len(Y_train)

	count = 0
	for i in range(len(Y_test)):
		prediction = weight.T.dot(X_test[i])
		if prediction > 0:
			print "HIT2"
			prediction = 1
		else:
			prediction = 0
		if prediction == Y_test[i]:
			count += 1
	print count
	print "Testing Error is", float(count) / len(Y_test)

if __name__ == '__main__':
	main()
