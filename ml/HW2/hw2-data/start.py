#!/usr/bin/python
from __future__ import division
from numpy import *
from math import *
import pdb

def calcWeight(ng, lamda, Y_train, X_train, dimension, iteration = 1,step = -10000.0):
	printLL = False
	weight = array([0.0]*dimension)
	weight0 = 0
	oll = 0 #old log loss
	N = len(X_train)
	for i in range(iteration):
		# figure out weight[0]
		error = 0
		pred = dot(X_train,weight)+weight0
		for j in range(N):
			pred[j] = 1-1/(1+exp(pred[j]))
		weight0 +=  ng / N * sum(Y_train - pred)

		#this gives the overall dot product
		val = dot(X_train.T ,(Y_train - pred))/N
		weight += ng * (-lamda*weight + val)

		pred = dot(X_train,weight)+weight0
		total = 0
		prod = 1
		ll = 0 #log loss
		for j in range(N):
			P = 1.0/(1+exp(pred[j]))
			if Y_train[j] == 1:
				P = 1.0 - P
		 	total += log(P)
		ll = lamda/2*sum([w**2 for w in weight])-total/N
		if printLL:
			print ll
		if abs(ll - oll) < step:
			print "Stop at Iteration", i
			break
		oll = ll

		# count = 0
		# pred = dot(X_train,weight)+weight0	
		# for j in range(N):
		# 	pred[j] = 1-1/(1+exp(pred[j]))
		# 	result = 1
		# 	if pred[j] <= 0.5:
		# 		result = 0
		# 	if result == Y_train[j]:
		# 		count += 1
		# print "Training Acc is ", float(count) / len(Y_train)

	# print weight
	return weight,weight0

def perceptron(ng,X_train,Y_train,dimension,iteration = 1):
	N = len(Y_train)
	weight = array([0.0]*dimension)
	for i in range(iteration):
		for j in range(N):
			pred = dot (X_train[j],weight)
			if pred > 0:
				pred = 1
			else:
				pred = 0

	return weight

def main():
	# training_data = genfromtxt('train.txt', delimiter=',')
	training_data = genfromtxt('oversampled_train.txt', delimiter=',')
	Y_train = training_data[:,0]
	X_train = training_data[:, 1:]
	Y_test = genfromtxt('test_label.txt', delimiter=',')
	X_test = genfromtxt('test.txt', delimiter=',')
	N = len(Y_train)
	# clicks = (Y_test == 1).sum()
	# ng = 0.1
	# lamda = 0.3
	# weight,weight0 = calcWeight(ng,lamda,Y_train,X_train,54,1000,0.0005)
	# weight,weight0 = calcWeight(ng,0,Y_train,X_train,54,1000)

	# print "lambda 0 ll is", sum([w**2 for w in weight])

	# weight,weight0 = calcWeight(ng,0.3,Y_train,X_train,54,1000)

	# print "lambda 0.3 ll is", sum([w**2 for w in weight])

	# weight,weight0 = calcWeight(0.01,0.3,Y_train,X_train,54,5000)
	# pred = dot(X_test,weight)+weight0
	# total = 0
	# #left is true zero, right is true one
	# one = (0,0)
	# zero = (0,0)
	# for j in range(len(X_test)):
	# 	#P of Y = 0 given input and weight
	# 	P = 1.0/(1+exp(pred[j]))
	# 	if P < 0.5:
	# 		if Y_test[j] == 0:
	# 			one = (one[0]+1,one[1])
	# 		else:
	# 			one = (one[0],one[1]+1)
	# 	else:
	# 		if Y_test[j] == 0:
	# 			zero = (zero[0]+1, zero[1])
	# 		else:
	# 			zero = (zero[0], zero[1]+1)

	# print "One", one
	# print "Zero", zero
	for i in range(N):
		if(Y_train[i]) == 0:
			Y_train[i] = -1

	weight = perceptron(0.1,X_train,Y_train,54,1000)


	# count = 0
	# pred = dot(X_train,weight)+weight0	
	# for j in range(len(X_train)):
	# 	pred[j] = 1-1/(1+exp(pred[j]))
	# 	result = 1
	# 	if pred[j] <= 0.5:
	# 		result = 0
	# 	if result == Y_train[j]:
	# 		count += 1
	# print "Training Acc is ", float(count) / len(Y_train)

	# count = 0
	# pred = dot(X_test,weight)+weight0	
	# for j in range(len(X_test)):
	# 	pred[j] = 1-1/(1+exp(pred[j]))
	# 	result = 1
	# 	if pred[j] <= 0.5:
	# 		result = 0
	# 	if result == Y_test[j]:
	# 		count += 1
	# print "Testing Acc is ", float(count) / len(Y_test)

if __name__ == '__main__':
	main()
