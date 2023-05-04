
# render_template -  api uses to generate html 
# request - object we need for forms 
from flask import Flask, jsonify, request, redirect, render_template, flash
import pandas as pd 
import pickle
from scipy import spatial
import os 
import json
from recommend_GloVe.recommend_GloVe_average import recommend
from functools import wraps
import time

with open("./static/courses.json", "r") as courses_file:
    courses = json.load(courses_file)


app = Flask(__name__)

def timer(request):
	@wraps(request)
	def wrapper(*args, **kwargs):
		start = time.perf_counter()
		response = request(*args, **kwargs)
		end = time.perf_counter()
		run = end - start
		print(f"Time to find a recommendation: {run} sec")
		return response
	return wrapper

@app.route('/')
def index():
    return render_template('index.html') 

@app.route('/rec',methods=['POST'])
@timer
def getvalue():
	try:
		coursename = request.form['search'].split(" ")[0]
		lowlvl = 'lowlvl' in request.form
		dept_filter = 'dept_filter' in request.form
		df = recommend([coursename], blacklist_lowerlevel=lowlvl, blacklist_dept=dept_filter)
		return render_template('result.html', tables = df, course = coursename)
	except Exception as e:
		error = "Invalid Course ID. Please Try Again"
		return render_template('index.html', error = error) 

@app.route('/search', methods=['POST'])
@timer
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
