import math
def CalcInfoGain(data,attIndex,resultIndex,thresholdIndex):
	t = f = 0
	#count the number of true and false
	for d in data:
		if(d[resultIndex] is True):
			t+=1
		else:
			f+=1
	t = float(t)/len(data)
	f = float(f)/len(data)
	print t, f
	H = 0
	if t > 0:
		H -= (t*math.log(t,2))
	if f > 0:
		H -= (f*math.log(f,2))
	print H
	data.sort(key=lambda tup: tup[attIndex])
	print data
	threshold = float(data[thresholdIndex][attIndex] + data[thresholdIndex-1][attIndex])/2
	left = (0,0)
	right = (0,0)
	for d in data:
		if d[attIndex] < threshold:
			if d[resultIndex] is True:
				left = (left[0] + 1, left[1])
			else:
				left = (left[0], left[1]+1)
		else:
			if d[resultIndex]:
				right = (right[0] + 1, right[1])
			else:
				right = (right[0], right[1]+1)
	print "Left has: ", left
	print "Right has: ", right
	Pt = float(sum(left))/(sum(left)+sum(right))
	Pf = float(sum(right))/(sum(left)+sum(right))
	HYX = 0
	Vt = 0
	if sum(left) != 0:
		if(left[0] != 0):
			Vt += float(left[0])/sum(left) * math.log(float(left[0])/sum(left))
		if (left[1] != 0): 
			float(left[1])/sum(left) * math.log(float(left[1])/sum(left))
	HYX=Pt*Vt
	if sum(right) != 0:
		if (right[0] != 0):
			Vt += float(right[0])/sum(right) * math.log(float(right[0])/sum(right))
		if (right[1] != 0):
			float(right[1])/sum(right) * math.log(float(right[1])/sum(right))
	HYX += Pf*Vt
	print "IG is: ", (H - HYX)
	return (H - HYX)

def main():
	ages = [24,53,23,25,32,52,22,43,52,48]
	salaries = [40000,52000,25000,77000,48000,110000,38000,44000,27000,65000]
	degrees = [True, False, False, True, True, True, True, False,False,True]
	data = zip(ages,salaries,degrees)
	return data

if __name__ == '__main__':
 	data = main()
 	max = 0
 	best = (0,0)
 	for i in range(2):
 		for j in range(1,len(data)):
 			v = CalcInfoGain(data,i,2,j)
 			if v > max:
 				max = v
 				best = (i,j)
 	print max, best
