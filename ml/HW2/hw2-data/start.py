#!/usr/bin/python
from __future__ import division
from numpy import *
from math import *

def calcWeight(ng, lamda, Y_train, X_train, dimension, iteration = 1000):

	weight = zeros((dimension,1),dtype=float)
	# figure out weight[0]
	for y in Y_train:
		weight[0] += ng * y/2

	for i in range(iteration):
		for j in range(1,dimension):
			# v is the sum of xj(yj - P(Yj=1|xj,w))
			v = 0
			for k in range(len(X_train)):
				s = weight[0] + sum(weight[1:].T.dot(X_train[k]))
				try:
					v += X_train[k][j-1] * (Y_train[k] - exp(s)/(1+exp(s)))
				except:
					print s
				# print "s is", s
				# print "v is", v

			weight[j] += ng * (-lamda*weight[j]+v)
			print "Weight at", j, " is", weight[j]

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

	calcWeight(ng,lamda,Y_train,X_train,55)

if __name__ == '__main__':
	main()
