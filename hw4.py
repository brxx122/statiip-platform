#-*-coding:UTF-8-*-
import pycrfsuite
import unicodedata
import pickle
import codecs
import random

templates = (
    (('c', -2), ),
    (('c', -1), ),
    (('c',  1), ),
    (('c',  2), ),
    (('c', 0), ('c', 1)),
    (('c', -1), ('c', 0)),
    (('c', -2), ('c', -1)),
    (('c', -1), ('c',  0), ('c',  1)),
    )
	
# Return whether the given character is punctuation.
# Specifically, whether it is a member of a Unicode 
# punctuation character class.
def is_punct(c):
	punct_categories = ['Pc', 'Pd', 'Pe', 'Pf', 'Pi', 'Po', 'Ps']
	#c = c.decode('utf-8')
	if c == '':
		return "0"
	if unicodedata.category(c) in punct_categories:
		return "1"
	else:
		return "0"

# Return whether the given character's "class", where
# class = 1 if numeric, 2 if english letter, 3 otherwise.
def char_class(c):
	num_categories = ['Nl', 'No', 'Nd']
	letter_categories = ['LC', 'Ll', 'Lm', 'Lm', 'Lo', 'Lt', 'Lu' ]
	#cat = unicodedata.category(c.decode('utf-8'))
	cat = unicodedata.category(c)
	if cat in num_categories:
		return "1"
	elif cat in letter_categories:
		return "2"
	else:
		return "3"

# generate feature
# input: ["现","在","种","田","省","心","多","了"] utf8
# output: [
# 	['c[1]=在','c[2]=种','c[0]|c[1]=现|在','punct=0','class=2'],
#	['c[-1]=现','c[1]=种','c[2]=田,'c[0]|c[1]=在|种',c[-1]|c[0]=现|在,'c[-1]|c[0]|c[1]=现|在|种','punct=0','class=2'],
#	...
#	[c[-2]=心','c[-1]=多','c[-1]|c[0]=多|了','c[-2]|c[-1]=心|多','punct=0','class=2']
#	]
def generate_feature(sent):
	feature = []
	length = len(sent)
	for i in range(length):
		f = []
		if i - 2 >= 0:
			f.append('c[-2]=' + sent[i - 2])
			f.append('c[-2]|c[-1]=' + sent[i-2] + '|' + sent[i-1])
		if i - 1 >= 0:
			f.append('c[-1]=' + sent[i - 1])
			f.append('c[-1]|c[0]=' + sent[i-1] + '|' + sent[i])
		if i + 1 < length:
			f.append('c[1]=' + sent[i + 1])
			f.append('c[0]|c[1]=' + sent[i] + '|' + sent[i + 1])
		if i + 2 < length:
			f.append('c[2]=' + sent[i + 2])
		if i - 1 >= 0 and i + 1 < length:
			f.append('c[-1]|c[0]|c[1]=' + sent[i-1] + '|' + sent[i] + '|' + sent[i + 1])
		f.append('punct=' + is_punct(sent[i]))
		f.append('class=' + char_class(sent[i]))
		feature.append(f)
	return feature
		

# use crf to tag sents
# input: "现在种田省心多了\n模范行动带新兵"
# output: ["BEBEBESS","BEBESBE"]
def sent2tag(str):
	tagger = pycrfsuite.Tagger()
	tagger.open('data/hw4/crf_open.model')
	sents = str.split('\n')
	label = []
	for i in range(len(sents)):
		sent = sents[i]
		if sent:
			feature = generate_feature(sent)
			label.append(tagger.tag(feature))
		else:
			del sents[i]
	return sents, label
			
# translate tag to words
# input: sents = ["现在种田省心多了","模范行动带新兵"], label = ["BEBEBESS","BEBESBE"]
# output: "现在 种田 省心 多 了\n模范 行动 带 新兵"
def tag2words(sents, labels):
	str = ""
	for i in range(len(sents)):
		sent = sents[i]
		label = labels[i]
		for j in range(len(sents[i])):
			str += sent[j]
			if label[j] == 'E' or label[j] == 'S':
				str += ' / '
		str += "\n"
	return str
	
def new_detect(str):
	result = ''
	str = str.strip().replace('\n', ' ')
	str = str.replace(' / ',' ')
	str = str.replace('/', ' ')
	words= str.split(' ')
	words = set(words)
	file = open('data\\hw4\\voc.pickle', 'rb')
	train_dict = pickle.load(file)
	for w in words:
		if w not in train_dict:
			result += w + '\t'
	return result
	
# using crf to segment texts
# input: "现在种田省心多了。模范行动带新兵" unicode
# output: "现在 种田 省心 多 了 。\n模范 行动 带 新兵"
def show_crf(str):
	text = ""
	for c in str:
		text += c
		if is_punct(c) == "1":
			text += '\n'
	sents, labels = sent2tag(text)
	result = tag2words(sents, labels)
	return result

def show_perm():
	close = [[0.958742, 0.948760, 0.953480, 0.9630, 0.4650],
	[0.958905, 0.950059, 0.954272, 0.9638, 0.4736],
	[0.959646, 0.951225, 0.955229, 0.9640, 0.4765]]
	open = [[0.972526, 0.964364, 0.968320, 0.977199, 0.574652],
	[0.972616, 0.966113, 0.969285, 0.9780, 0.5799],
	[0.973986, 0.966715, 0.970252, 0.9784,0.5828]]
	name = ['feature1','feature2','feature3']
	return name, close, open

def show_new(str):
	segment = show_crf(str)
	new_words = new_detect(segment)
	if new_words == '':
		new_words = u'没有新词'
	return segment, new_words

def show_wrong():
	file = codecs.open('data\\hw4\\wrong_words.txt', 'r', encoding='utf-8')
	sents = []
	pair = []
	str = ''
	for line in file:
		if line == '\r\n' or line == '\n':
			pair.append(line)
			sents.append(pair)
			pair = []
		else:
			pair.append(line)
	for i in range(5):
		idx = int(random.random() * len(sents))
		str += '--------------------------------------------\n'.join(sents[idx])
	return str