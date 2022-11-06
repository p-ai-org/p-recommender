# a speedy walk through of how we made the mvp!

### Set up app.py framework 
- import flask + requisite functions (render_framework, request)
	- render_framework is what the api uses to generate html with inbuilt jinja2 template formatting 
	- request is what allows us to talk with the data the client sends to the server (acts like a global object)
- Include our rec function 
- Add flask skeleton components (app = Flask(__name__) to app.py, template folder, static/stylesheets, etc)
- We have two html pages: an index page where the user puts in the data and the results page which the top x results
	- @app.route('/') --> returns index.html
	- @app.route('/'rec) --> uses user data from index.html page and calls our rec function >> returns results.html page 

### Set up index.html 
- Set up html form 
	- post method
	- action 
	- text input from user
	- submit button 

### Set up request.html
- loop through panda df using jinja2 for loops syntax 