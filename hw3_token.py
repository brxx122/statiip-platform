#coding: utf-8
from __future__ import division
import re
import random
import pickle
from collections import defaultdict
from numpy import *

# prob_emit:B
# prob_start: pi
# prob_trans: A

signName = ['B', 'E', 'M', 'S']

def d():
	return defaultdict(int)
	
def splitsent(text):
	text = text.replace('\n','')
	str = "[，。、：！；（）“”《》？——\‘’{}【】~-]".decode('utf-8')
	strRegex = re.compile(str)
	sents = strRegex.split(text)
	return sents
	
def Viterbi(sent,prob_emit,prob_start,prob_trans):
	if(sent == ""):
		return -1
	sents = list(sent)
	T = len(sents)
	delta = []
	delta.append(-1)
	path = []
	path.append(-1)
	temp = []
	for i in range(4):
		if(prob_start[signName[i]]):
			pi = log(prob_start[signName[i]])
		else:
			pi = -3.14e+100
		if(sents[0] not in prob_emit[signName[i]]):
			if(i == 3):
				b = log(1.0)
			else:
				b = -3.14e+100
		else:
			if(prob_emit[signName[i]][sents[0]]):
				b = log(prob_emit[signName[i]][sents[0]])
			else:
				b = -3.14e+100
		temp.append(pi + b)
	delta.append(temp)			##log
	path.append([0,0,0,0])
	
	for t in range(2, T + 1):		#[2, T]
		state = []
		laststate = []
		for i in range(4):		# for each state in t
			temp = []
			for j in range(4):		#for each state in t-1
				if (prob_trans[signName[j]][signName[i]]):
					a = log(prob_trans[signName[j]][signName[i]])
				else:
					a = -3.14e+100
				temp.append(delta[t-1][j] + a)		##log
			if (sents[t-1] not in prob_emit[signName[i]]):
				if (i == 3):	#Single
					b = log(1.0)
				else:
					b = -3.14e+100
			else:
				if (prob_emit[signName[i]][sents[t-1]]):
					b = log(prob_emit[signName[i]][sents[t-1]])
				else:
					b = -3.14e+100
			state.append(max(temp) + b)
			laststate.append(argmax(temp))
		delta.append(state)
		path.append(laststate)
	
	P = max(delta[T])
	S = [0] * (T + 1)
	S[T] = argmax(delta[T])
	
	for t in range(T-1, 0, -1):		#[T-1, 1]
		S[t] = path[t+1][S[t+1]]
	
	return S[1:]

def sents_token(sent, state):
	sent = list(sent)
	tokens = ""
	for i in range(len(state)):
		tokens += sent[i]
		if(state[i] == 1 or state[i] == 3):
			tokens += u" / "
	words = tokens.split(u' ')
	return words, tokens

def Token(testText,emit,start,trans):
	sents = splitsent(testText)
	str = ""
	for i in range(len(sents)):
		state = Viterbi(sents[i],emit,start,trans)
		if(state == -1):
			continue
		words, result = sents_token(sents[i], state);
		str = str + result + "\n"
	return str

def show_prob(Text):
	f = open("data/hw3/chinesetoken/prob_para.txt")
	emit, trans, start = pickle.load(f)
	f.close()
	str = Token(Text,emit,start,trans)
	return str
	
def show_P(Text):
	f = open("data/hw3/chinesetoken/P_para.txt")
	emit, trans, start = pickle.load(f)
	f.close()
	str = Token(Text,emit,start,trans)
	return str
	
def load_result():
	name = [u'初始参数',u'有监督算法']
	x1 = array([0.636905732732,0.703858547758,0.668710452125])
	x2 = array([0.634250270546,0.70252868903,0.666645757538])
	x3 = array([0.636192652906,0.704013348555,0.668386978435])
	x4 = array([0.633092839208,0.700257512238,0.664983537326])
	x5 = array([0.634576019348,0.700827470628,0.66605832604])
	
	y1 = array([0.646600180602,0.704018122047,0.674088665865])
	y2 = array([0.645072092431,0.703143295777,0.672857053929])
	y3 = array([0.642386654921,0.698049344176,0.669062280448])
	y4 = array([0.642758954963,0.699514013196,0.669936602717])
	y5 = array([0.642503181139,0.698606122063,0.669381167839])
	
	result = zeros([2,3])
	result[0,:] = list((x1 + x2 + x3 + x4 + x5) / 5)
	result[1,:] = list((y1 + y2 + y3 + y4 + y5) / 5)
	return name, list(result)