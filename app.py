

from flask import Flask, render_template, request
import pandas as pd


app = Flask(__name__)


#function to get recs
def get_recs(course_title):
    result = [course_title for i in range(1, 10)]
    #result = pd.DataFrame(result)
    return result


@app.route('/')
def index():
    return render_template('index.html')


#results in file routing 

@app.route('/rec', methods = ['POST'])
def rec_page():
    coursename = request.form['coursename']
    result = get_recs(coursename)
    return render_template("results.html", coursename = coursename, result = result)




if __name__ == '__main__':
    app.run()






