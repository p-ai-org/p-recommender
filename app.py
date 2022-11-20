
# render_template -  api uses to generate html 
# request - object we need for forms 
from flask import Flask, jsonify, request, redirect, render_template
import pandas as pd 
import pickle
from scipy import spatial
import os 
import json

with open('description_embeddings.pickle', 'rb') as handle:
    description_embeddings = pickle.load(handle)

with open("./static/courses.json", "r") as courses_file:
    courses = json.load(courses_file)

def recommend(user_input):
    def similarity(user_input, reference):
        return 1 - spatial.distance.cosine(description_embeddings[user_input.upper()], description_embeddings[reference])  

    def closest_courses(user_input):
        unsorted = [ (course, round(similarity(user_input, course), 2), [x for x in courses if x["identifier"] == course][0])
                    for course in description_embeddings.keys()]
        return sorted(unsorted, key = lambda w: w[1], reverse = True)
    
    if type(user_input) == str:
        if not (user_input in description_embeddings):
            raise ValueError("user_input must be a valid id")
        return closest_courses(user_input)[1:11]
    elif type(user_input) == list:
        unsorted = []
        for ui in user_input:
            if ui in description_embeddings:
                unsorted += closest_courses(ui)[1:6]

        if len(unsorted) < 2:
            raise ValueError("At least two id in user_input must be valid id")
        return sorted(unsorted, key = lambda w: w[1], reverse = True)[:10]
    else:
    	raise ValueError("user_input must be a string or list of strings")

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html') 

@app.route('/rec',methods=['POST'])
def getvalue():
    coursename = request.form['search'].split(" ")[0]
    df = recommend(coursename)
    return render_template('result.html', tables = df, course = coursename)

@app.route('/search', methods=['POST'])
def search():
	term = request.form['q']
	print ('term: ', term)
	
	SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
	json_url = os.path.join(SITE_ROOT, "data", "newresults.json")
	json_data = json.loads(open(json_url).read())
	#print (json_data)
	#print (json_data[0])

	filtered_dict = [v for v in json_data if (term in v or string.capwords(term) in v)]	
	# print(filtered_dict)
	
	resp = jsonify(filtered_dict)
	resp.status_code = 200
	print(resp)
	return resp

if __name__ == '__main__':
    app.run(debug=True)