

from flask import Flask, render_template, request
import pandas as pd


app = Flask(__name__)


#function to get recs
def get_recs(course_title):
    result = [course_title for i in range(1, 10)]
    result = pd.DataFrame(result, columns = "Recs")
    return result


@app.route('/')
def index():
    return render_template()



def main():
    return "Hello Claremont! Welcome to p-recommender."

if __name__ == '__main__':
    app.run()


