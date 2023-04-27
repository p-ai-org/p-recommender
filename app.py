
# render_template -  api uses to generate html 
# request - object we need for forms 
from flask import Flask, jsonify, request, redirect, render_template, flash
import pandas as pd 
import pickle
from scipy import spatial
import os 
import json

from recommend_tfidf.recommend_tfidf import recommend
# from recommend_GloVe.recommend_GloVe_average import recommend


with open("./static/courses.json", "r") as courses_file:
    courses = json.load(courses_file)


app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/rec',methods=['POST'])
def getvalue():
	try:
		user_input = request.form['search']
		upperlvl = 'upperlvl' in request.form
		cmc = 'cmc' in request.form
		pomona = 'pomona' in request.form
		hmc = 'hmc' in request.form
		scripps = 'scripps' in request.form	
		pitzer = 'pitzer' in request.form
		other = 'other' in request.form
		df = recommend(user_input, upperlvl=upperlvl, cmc=cmc, pomona=pomona, hmc=hmc, scripps=scripps, pitzer=pitzer, other=other)
		return render_template('result.html', tables = df, course = user_input)
	except Exception as e:
		print(e)
		error = "Invalid Description. Please Try Again"
		return render_template('index.html', error = error) 

@app.route('/search', methods=['POST'])
def search():
	term = request.form['q']
	print ('term: ', term)
	
	SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
	json_url = os.path.join(SITE_ROOT, "data", "newresults.json")
	json_data = json.loads(open(json_url).read())
	#print (json_data)
	#print (json_data[0])

	filtered_dict = [v for v in json_data if term.lower() in v.lower()]
	# print(filtered_dict)
	
	resp = jsonify(filtered_dict)
	resp.status_code = 200
	print(resp)
	return resp

if __name__ == '__main__':
    app.run(debug=True)
