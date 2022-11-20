from flask import Flask, render_template, request 
import pandas as pd


app = Flask(__name__)

#function to get recs
def get_recs(course_title):
    # global result
    result = [course_title for i in range(1, 10)]
    # result = pd.DataFrame(result)
    return result

#index file routing
@app.route('/')

def index():
    return render_template("index.html")

# results file routing
@app.route('/rec', methods=['POST'])
def rec_page():
    coursename = request.form["coursename"]
    result = get_recs(coursename)
    #tables = [result.to_html(classes='data')],
    return render_template("results.html", result=result, coursename = coursename)

# def main():
#     return "Hello Claremont! Welcome to p-recommender."

# if __name__ == '__main__':
#     app.run()