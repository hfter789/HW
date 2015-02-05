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

		for j in range(1,dimension):
			# v is the sum of xj(yj - P(Yj=1|xj,w))
			v = 0
			for k in range(N):
				s = weight.T.dot(X_train[k])
				v += X_train[k][j] * (Y_train[k] - exp(s)/(1+exp(s)))
				# print "s is", s
				# print "v is", v
			#pdb.set_trace()
			weight[j] += ng * (-lamda*weight[j]+v/N)
			# print "Weight at", j, " is", weight[j]
		
		#p = 1
		#for x in X_train:
		#	p = p * 1/(1+exp(weight.T.dot(x)))
		#if p != 0:
		#	print lamda / 2 * sum([w**2 for w in weight]) - log(p)/N
		#else:
		#	print lamda / 2 * sum([w**2 for w in weight])
			count = 0
		for i in range(len(Y_train)):
			s = weight.T.dot(X_train[i])
			prediction = exp(s)/(1+exp(s))
			res = 0
			if prediction > 0.5:
				res = 1
			if res == Y_train[i]:
				count += 1
		#print count
		print "Prediction is",prediction, "Training Acc is ", float(count) / len(Y_train)

	print weight
	return weight

def main():
	training_data = genfromtxt('train.txt', delimiter=',')
	Y_train = training_data[:,0]
	X_train = training_data[:, 1:]
	Y_test = genfromtxt('test_label.txt', delimiter=',')
	X_test = genfromtxt('test.txt', delimiter=',')

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
