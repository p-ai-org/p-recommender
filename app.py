
from flask import Flask, render_template, request
import pandas as pd 

app = Flask(__name__)


#function to get recs
def get_recs(course_title):
    # global result
    result = [course_title for i in range(1, 10)]
    result = pd.DataFrame(result)
    return result 

# index file routing 
@app.route('/', methods=["POST", "GET"])
def index():
    if request.method == "GET":
        languages = ["C++", "Python", "PHP", "Java", "C", "Ruby",
                     "R", "C#", "Dart", "Fortran", "Pascal", "Javascript"]
          
    return render_template("index.html", languages=languages)
  

# results file routing 
@app.route('/rec', methods = ['POST'])
def rec_page():
    coursename = request.form["coursename"]
    # result = get_recs(coursename)
    return render_template("results.html", coursename = coursename)