#-*-coding:UTF-8-*-
from numpy import *
import re
import random

def textParse(string):
	Tokens = re.split(r'[^A-Za-z_]*', string);
	return [tok.lower() for tok in Tokens if len(tok) > 0]

def loadtext():
	docText = [];
	docList = [];
	List1 = [];
	List0 = [];
	classList = [];
	for i in range(1,26):	#without 26
		temp = open('data/hw1/email/spam/%d.txt' % i).read();
		docText.append(temp);
		wordList = textParse(temp);
		docList.append(wordList);
		List1.extend(wordList);
		classList.append(1);
		temp = open('data/hw1/email/ham/%d.txt' % i).read();
		docText.append(temp);
		wordList = textParse(temp);
		docList.append(wordList);
		List0.extend(wordList);
		classList.append(0);
	return docText,docList,List1,List0,classList

def createVoc(docList):
	Vocset = set([]);
	for doc in docList:
		Vocset = Vocset | set(doc);
	return list(Vocset)
	
def wordbag(Vocset, inputdoc):
	word = [0] * len(Vocset);
	for v in inputdoc:
		if v in Vocset:
			word[Vocset.index(v)] += 1;
		else:
			print "The word isn't in the Vocabulary"
	return word
	
def trainNB(trainingMat, trainingClass,V):
	wordNum = len(trainingMat[0]);
	num0 = wordNum * [0];
	num1 = wordNum * [0];
	sum0 = 0.0; sum1 = 0.0;
	p1Vec = zeros(wordNum);
	p0Vec = zeros(wordNum);
	for i in range(0, len(trainingMat)):
		if trainingClass[i] == 1:
			num1 += trainingMat[i];
			sum1 += sum(trainingMat[i]);
		else:
			num0 += trainingMat[i];
			sum0 += sum(trainingMat[i]);
	sum1 += V;
	sum0 += V;
	num1 = array(num1) + 1;
	num0 = array(num0) + 1;
	p1Vec = log(num1) - log(sum1);
	p0Vec = log(num0) - log(sum0);
	return p1Vec,p0Vec;

def classifyNB(testMat, p1Vec, p0Vec,Ps, Ph):
	p1 = sum(testMat * p1Vec) + Ps;
	p0 = sum(testMat * p0Vec) + Ph;
	if p1 > p0:
		return 1;
	else:
		return 0;

def testfunc(tp,tn,fp,fn):
	str = ""; 
	Precision = float(tp) / float(tp + fp);
	Recall = float(tp) / float(tp + fn);
	F = (2 * Precision * Recall) / (Precision + Recall);
	Error = float(fp + fn) / float(tp + tn + fp + fn);
	str += "\nThe Error rate is %f\n" % Error;
	str += "The Precision rate is %f\n" % Precision;
	str += "The Recall rate is %f\n" % Recall;
	str += "The F rate is %f\n" % F;
	return str;
	
def spamtrain():
	docText,docList,List1,List0,classList = loadtext();
	Ps = log(len(List1) / float(len(List1) + len(List0)));
	Ph = log(len(List0) / float(len(List1) + len(List0)));
	VocList = createVoc(docList);
	V = len(VocList);
	
	#divide dataset between training and test 
	trainingSet = range(0,50);
	testSet = [];
	for i in range(10):
		randIndex = int(random.uniform(0,len(trainingSet)));
		testSet.append(trainingSet[randIndex]);
		del(trainingSet[randIndex]);
	
	#create training dataset	
	trainingMat = [];
	trainingClass = [];
	for i in trainingSet:
		trainingMat.append(wordbag(VocList, docList[i]));
		trainingClass.append(classList[i]);
	p1Vec, p0Vec = trainNB(array(trainingMat), array(trainingClass),V);
		
	#create test dataset
	testMat = [];
	testClass = [];
	tp = 0; fp = 0; fn = 0; tn = 0;
	str = "";
	strr = "";
	for i in testSet:
		testMat = wordbag(VocList, docList[i]);
		testclass = classifyNB(array(testMat), p1Vec, p0Vec,Ps, Ph);
		if testclass == 1 and classList[i] == 1:
			tp = tp + 1;
		elif testclass == 1 and classList[i] == 0:
			fp = fp + 1;
			str = "********The following email should be ham, but is selected as spam email.********\n"
			str += docText[i].decode('ISO-8859-2');
			str +=  "\n*********************************************************************************"
			str += "\n";
		elif testclass == 0 and classList[i] == 1:
			fn = fn + 1;
			str = "********The following email should be spam, but is selected as ham email.********\n"
			str += docText[i].decode('ISO-8859-2');
			str += "\n*********************************************************************************"
			str += "\n";
		else:
			tn = tn + 1;
	strr += testfunc(tp,tn,fp,fn)
	return strr,str,fn,fp

def Looptesting():
	count = 0;
	strr = "";
	for i in range(0, 100):
		docText, docList, List1, List0, classList = loadtext();
		Ps = log(len(List1) / float(len(List1) + len(List0)));
		Ph = log(len(List0) / float(len(List1) + len(List0)));
		VocList = createVoc(docList);
		V = len(VocList);

		# divide dataset between training and test
		trainingSet = range(0, 50);
		testSet = [];
		for i in range(10):
			randIndex = int(random.uniform(0, len(trainingSet)));
			testSet.append(trainingSet[randIndex]);
			del (trainingSet[randIndex]);

		# create training dataset
		trainingMat = [];
		trainingClass = [];
		for i in trainingSet:
			trainingMat.append(wordbag(VocList, docList[i]));
			trainingClass.append(classList[i]);
		p1Vec, p0Vec = trainNB(array(trainingMat), array(trainingClass), V);

		# create test dataset
		testMat = [];
		testClass = [];
		tp = 0;
		fp = 0;
		fn = 0;
		tn = 0;
		for i in testSet:
			testMat = wordbag(VocList, docList[i]);
			testclass = classifyNB(array(testMat), p1Vec, p0Vec, Ps, Ph);
			if testclass == 1 and classList[i] == 1:
				tp = tp + 1;
			elif testclass == 1 and classList[i] == 0:
				fp = fp + 1;
			elif testclass == 0 and classList[i] == 1:
				fn = fn + 1;
			else:
				tn = tn + 1;
		if fn != 0 or fp != 0:
			count = count + 1;
			print  "fn = %d,fp = %d\n" % (fn,fp)
	strr = "The total error rate is %f" % (count / float(100));
	return strr
	
	
		