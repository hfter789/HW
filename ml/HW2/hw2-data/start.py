#!/usr/bin/python
from __future__ import division
from numpy import *
from math import *
import pdb

def calcWeight(ng, lamda, Y_train, X_train, dimension, iteration = 1):

	weight = arange(dimension)
	weight0 = 0

	N = len(X_train)
	for i in range(iteration):
		# figure out weight[0]
		error = 0
		# for j in range(N):
		# 	s = weight0 + weight.T.dot(X_train[j])
		# 	error += Y_train[j] - exp(s)/(1+exp(s))
		pred = dot(X_train,weight)+weight0
		for j in range(N):
			pred[j] = 1-1/(1+exp(pred[j]))
		weight0 +=  ng / N * sum(Y_train - pred)

		#this gives the overall dot product
		val = dot(X_train.T ,(Y_train - pred))/N
		weight += ng * (-lamda*weight + val)

		count = 0
		pred = dot(X_train,weight)+weight0	
		for j in range(N):
			pred[j] = 1-1/(1+exp(pred[j]))
			result = 1
			if pred[j] <= 0.5:
				result = 0
			if result == Y_train[j]:
				count += 1
		# print "Training Acc is ", float(count) / len(Y_train)

	# print weight
	return weight

def main():
	training_data = genfromtxt('train.txt', delimiter=',')
	Y_train = training_data[:,0]
	X_train = training_data[:, 1:]
	Y_test = genfromtxt('test_label.txt', delimiter=',')
	X_test = genfromtxt('test.txt', delimiter=',')

	ng = 0.1
	lamda = 0.3
	weight = calcWeight(ng,lamda,Y_train,X_train,54,1000)

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
