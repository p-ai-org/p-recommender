from flask import Flask, render_template, request
import pandas as pd
app = Flask(__name__) # needs to be second line

#function to get recs
def get_recs(title):
    # global result
    result = [title for i in range(10)]
    result = pd.DataFrame(result)
    return result


@app.route('/')
def index():
    return render_template("index.html")
#def main():
#   return "Hello Claremont! Welcome to p-recommender."



@app.route('/rec', methods=['POST'])
def rec():
    coursename = request.form["coursename"]
    #result = get_recs(coursename)
    return render_template("results.html", coursename = coursename)




if __name__ == '__main__':
    app.run()