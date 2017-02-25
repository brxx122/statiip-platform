#-*-coding:UTF-8-*-
from __future__ import print_function
from flask import Flask, render_template, session, request, redirect, flash, g
from time import sleep
import sys
import json
import hashlib
import chartkick
import hw1
import hw1_extra
import hw2
import hw3_token
import hw3_share
import hw4

#app=Flask(__name__,static_folder=chartkick.js(), static_url_path='/static/js')
app=Flask(__name__)
app.jinja_env.add_extension("chartkick.ext.charts")
app.secret_key ='123456'

@app.route('/')
def page_base():
	return render_template('introduction.html')

@app.route('/hw1')
def page_hw1():
	return render_template('hw1.html')
	
@app.route('/hw1',methods=['POST'])
def hw1_train():
	action = request.form['submit']
	if action == "start":
		str_start,str_text,fn,fp = hw1.spamtrain();
		return render_template('hw1.html',result1 = str_start,text = str_text)
	elif action == "loop":
		str_loop = hw1.Looptesting();
		return render_template('hw1.html',result1 = str_loop)
	elif action == "start2":
		plt = hw1_extra.load_TF()
		plt1,plt2 = hw1_extra.rate()
		result2 = "Threshold = 0.0003\nError rate is 0.032370\nF rate is 0.976510\nThe number of Voc is 4463\n"
		result2_1 = hw1_extra.load_result()
		return render_template('hw1.html',TF_IDF = plt, error = plt1, F = plt2, result2 = result2, result2_1 = result2_1)
	else:
		return render_template('hw1.html')
	
@app.route('/hw2')
def page_hw2():
	session['ng'] = 0;
	session['webkb'] = 0;
	return render_template('hw2.html')

@app.route('/hw2',methods=['POST'])
def hw2_train():
	action = request.form['submit']
	if action == "ng":
		hw2_plt1 = hw2.load_ng()
		session['ng'] = 1
		hw2_plt2 = []
		if session['webkb'] == 1:
			hw2_plt2 = hw2.load_webkb()
		return render_template('hw2.html', ng = hw2_plt1, webkb = hw2_plt2)
	elif action == "webkb":
		hw2_plt2 = hw2.load_webkb()
		session['webkb'] = 1;
		hw2_plt1 = []
		if session['ng'] == 1:
			hw2_plt1 = hw2.load_ng()
		return render_template('hw2.html', ng = hw2_plt1 ,webkb = hw2_plt2)
	elif action == "r8r32":
		r8_name, r8, r52_name, r52 = hw2.load_r8r32()
		hw2_plt1 = []
		hw2_plt2 = []
		if session['ng'] == 1:
			hw2_plt1 = hw2.load_ng()
		if session['webkb'] == 1:
			hw2_plt2 = hw2.load_webkb()
		return render_template('hw2.html', ng = hw2_plt1 ,webkb = hw2_plt2, r8_name=r8_name, r8=r8, r52_name=r52_name, r52=r52)
	else:
		return render_template('hw2.html')

@app.route('/hw3_token')
def page_hw3_token():
	session['prob_fg'] = 0;
	session['P_fg'] = 0;
	return render_template('hw3_token.html')

@app.route('/hw3_token',methods=['POST'])
def hw3_token_train():
	action = request.form['submit']
	Text = request.form.get('Text')
	prob_str, P_str, input = "", "", ""
	if action == "prob":
		if(len(Text) != 237):
			input = Text
		prob_str = hw3_token.show_prob(Text)
		session['prob'] = prob_str
		session['prob_fg'] = 1
		if session['P_fg'] == 1:
			P_str = session['P']
		return render_template('hw3_token.html', input = input, prior = prob_str, NB = P_str)
	elif action == "P":
		if(len(Text) != 237):
			input = Text
		P_str = hw3_token.show_P(Text)
		session['P'] = P_str
		session['P_fg'] = 1
		if session['prob_fg'] == 1:
			prob_str = session['prob']
		return render_template('hw3_token.html',  input = input, prior = prob_str, NB = P_str)
	elif action == "result":
		name,result = hw3_token.load_result()
		return render_template('hw3_token.html', name = name, result = result)
	else:
		return render_template('hw3_token.html')
	
@app.route('/hw3_share')
def page_hw3_share():
	return render_template('hw3_share.html')
	
@app.route('/hw3_share',methods=['POST'])
def hw3_share_train():
	action = request.form['submit']
	if action == "result":
		a1, a2, name, three, five = hw3_share.load()
		return render_template('hw3_share.html', a1 = a1, a2 = a2, name = name, three_state = three, five_state = five, flag = 1)
	return render_template('hw3_share.html')
	
@app.route('/hw4')
def page_hw4():
	session['hmm_fg'] = 0;
	session['crf_fg'] = 0;
	return render_template('hw4.html', page = 0)

@app.route('/hw4',methods=['POST'])
def hw4_train():
	action = request.form['submit']
	Text = request.form.get('Text')
	hmm_str, crf_str, input = "", "", ""
	if action == "perform":
		name, close, open = hw4.show_perm()
		return render_template('hw4.html', page = 0, name = name, close = close, open = open)
	elif action == "discover":
		return render_template('hw4.html', page = 1)
	elif action == 'new_words':
		new_Text = request.form.get('New_text')
		new_input = new_Text
		segment, new_words = hw4.show_new(new_Text)
		return render_template('hw4.html', page = 1, new_input = new_Text, segment = segment, new_words = new_words)
	elif action == "wrong":
		wrong = hw4.show_wrong()
		return render_template('hw4.html', page = 2, wrong = wrong)
	elif action == "hmm":
		if(len(Text) != 237):
			input = Text
		hmm_str = hw3_token.show_P(Text)
		session['hmm'] = hmm_str
		session['hmm_fg'] = 1
		if session['crf_fg'] == 1:
			crf_str = session['crf']
		return render_template('hw4.html', page = 0, input = input, hmm = hmm_str, crf = crf_str)
	elif action == "crf":
		if(len(Text) != 237):
			input = Text
		crf_str = hw4.show_crf(Text)
		session['crf'] = crf_str
		session['crf_fg'] = 1
		if session['hmm_fg'] == 1:
			hmm_str = session['hmm']
		return render_template('hw4.html', page = 0,input = input, hmm = hmm_str, crf = crf_str)
	else:
		return render_template('hw4.html')
	return render_template('hw4.html')
	
if __name__ == '__main__':
	app.run(debug=True)
	'''print('oh hello')
    #sleep(10)
    sys.stdout.flush()
    app.run(host="localhost", port = 8000)'''
