import math
#the program assumes that the last field of the turple is the output.

def calcInfoGain(data, index,resultIndex):
	#discrete or continuous, assume continuous for now
	#calculate H(D)
	t = f = 0
	for d in data:
		if(d[resultIndex] is True):
			t+=1
		else:
			f+=1
	left = (0,0)
	right = (t,f)
	t = float(t)/len(data)
	f = float(f)/len(data)
	print t, f
	H = -(t*math.log(t,2))-(f*math.log(f,2))
	print H
	maxIG = 0
	data.sort(key=lambda tup:tup[index])
	for i in range(1,len(data)):
		if(data[i-1][index] == data[i][index]):
			if(data[i][resultIndex] is True):
			left = (left[0] + 1, left[1])
			right = (right[0] - 1, right[1])
			continue;
		threshold = (data[i][index] + data[i-1][index]) / float(2)
		print threshold


def buildTree(data, numOfAtt,attRec):
	#record of attribute used
	infoGains = dict()
	root = dict()
	for i in range(numOfAtt):
		if i in attRec:
			continue;
		#calculate each individual attributes.
		calcInfoGain(data,i,numOfAtt)


def main():
	ages = [24,53,23,25,32,52,22,43,52,48]
	salaries = [40000,52000,25000,77000,48000,110000,38000,44000,27000,65000]
	degrees = [True, False, False, True, True, True, True, False,False,True]
	data = zip(ages,salaries,degrees)

	root = buildTree(data,2,set())

if __name__ == '__main__':
	main()