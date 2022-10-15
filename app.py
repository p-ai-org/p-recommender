from flask import Flask
app = Flask(__name__)


def get_recommendations(title):
    return None


@app.route('/')

def main():
    return "Hello Claremont! Welcome to p-recommender."

if __name__ == '__main__':
    app.run()