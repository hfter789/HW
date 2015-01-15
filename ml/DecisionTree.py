def calcInfoGain(data, index):
	#discrete or continuous

def buildTree(data, numOfAtt,attRec):
	#record of attribute used
	infoGains = dict()
	for i in range(numOfAtt):
		if i in attRec:
			continue;
		#calculate each individual attributes.
		calcInfoGain(data,i)


def main():
	ages = [24, 53,23,25,32,52,22,43,52,48]
	salaries = [40000,52000,25000,77000,48000,110000,38000,44000,27000,65000]
	degrees = [True, False, False, True, True, True, True, False,False,True]
	data = zip(ages,salaries,degrees)

	root = buildTree(data,2,set()
	


if __name__ == '__main__':
	main()



