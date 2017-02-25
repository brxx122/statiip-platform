from numpy import *

def load_ng():
	data1 = []
	data2 = []
	x = [20,40,100,200,300,500,800,1000,2000]
	y1 = [16.4,18.8,17.8,22.6,18,20.3,15.6,16.4,19.0]
	y2 = [17.8,23,22.8,22.6,18.4,22.19,14.4,16.4,22.6]
	for i in range(0,9):
		data1.append([x[i],y1[i]])
		data2.append([x[i],y2[i]])
	plt = [{'data':data1, 'name': 'No unlabeled documents'},{'data':data2, 'name': '5000 unlabeled documents'}]
	return plt
	
def load_webkb():
	data1 = []
	data2 = []
	x = [4,10,20,50,100,200]
	a = array([33.8,34.2,40,40.1,35.4,35.2])
	b = array([33.3,35.3,33.7,42.3,37.9,48.4])
	c = array([31.7,35.3,35.7,38,39.3,42.6])
	y1 = (a + b + c) / 3;
	y1 = list(y1);
	
	a = array([33.6,35.0,37.3,46.9,33.6,34.4])
	b = array([30.0,40.0,32.7,48.9,40.0,47.9])
	c = array([32.3,36.9,35.3,37.2,37.4,41.1])
	y2 = (a + b + c) / 3;
	y2 = list(y2);
	
	for i in range(0,6):
		data1.append([x[i],y1[i]])
		data2.append([x[i],y2[i]])
	plt = [{'data':data1, 'name': 'No unlabeled documents'},{'data':data2, 'name': '5000 unlabeled documents'}]
	return plt

def load_r8r32():
	lines = open('data/hw2/r8r52.txt').readlines()
	data = [line.strip().split('\t') for line in lines]
	r8_name = [w[0] for w in data[0:8]]
	r52_name = [w[0] for w in data[8:-1]]
	r8 = [[float(w[1]), float(w[2])] for w in data[:8]]
	r52 = [[float(w[1]), float(w[2])] for w in data[8:-1]]
	return r8_name, r8, r52_name, r52