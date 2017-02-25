def load_TF():
	data1 = open('data/hw1/Example_preProcess/TF_IDF0.txt').read()
	t = data1.replace("[","")
	t = t.replace("]","")
	temp = t.split(",")
	TF_IDF0 = [float(num) for num in temp]
	y0 = sorted(TF_IDF0)
	
	data2 = open('data/hw1/Example_preProcess/TF_IDF1.txt').read()
	t = data2.replace("[","")
	t = t.replace("]","")
	temp = t.split(",")
	TF_IDF1 = [float(num) for num in temp]
	y1 = sorted(TF_IDF1)
	
	S0 = [];
	S1 = [];
	for i in range(len(y1)):
		S0.append([i,y0[i]])
		S1.append([i,y1[i]])
	plt = [{'data':S0[83000:], 'name':'TF_IDF0'},{'data':S1[83000:], 'name':'TF_IDF1'}]
	return plt
	
def rate():
	error = [[0.001,0.047399],[0.0009,0.047399],[0.0008,0.049711],[0.0007,0.046243],[0.0006,0.042775],[0.0005,0.039306],[0.0004,0.033526],[0.0003,0.032370],[0.0002 ,0.034682]]
	F = [[0.001,0.965805],[0.0009,0.965805],[0.0008,0.950739],[0.0007,0.966611],[0.0006,0.968986],[0.0005,0.971524],[0.0004,0.975651],[0.0003,0.976510],[0.0002 ,0.974874]]
	return error,F
	
def load_result():
	data1 = open('data/hw1/Example_preProcess/spam.txt').read()
	data2 = open('data/hw1/Example_preProcess/ham.txt').read()
	t1 = data1.replace("[","")
	t1 = t1.replace("]","")
	temp1 = t1.split(",")
	t2 = data2.replace("[","")
	t2 = t2.replace("]","")
	temp2 = t2.split(",")
	str = "The total number of SPAM email is %d" % len(temp1)
	str += "\n" + t1[:100] + "...........\n"
	str += "*****************************************************************\nThe total number of HAM email is %d" % len(temp2)
	str += "\n" + t2[:100] + "..........."
	return str