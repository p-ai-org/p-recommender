
# render_template -  api uses to generate html 
# request - object we need for forms 
from flask import Flask, render_template,request
import pandas as pd 

#TODO: this is a stand in for an arbitrary rec function for now 
def get_recommendations(title):
    global result
    result = [title for i in range(1, 10)]
    result = pd.DataFrame(result, columns =['Recs'])
    return result 

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html') 

# Used to send HTML form data to the server. 
# The data received by the POST method is __not__ cached by the server.
@app.route('/rec',methods=['POST'])
def getvalue():
    coursename = request.form['coursename']
    get_recommendations(coursename)
    df=result
    return render_template('result.html',  tables=[df.to_html(classes='data')], titles=df.columns.values, course = coursename)

if __name__ == '__main__':
    app.run(debug=False)
