from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)


@app.route('/')
def welcome():  # put application's code here
    return 'Welcome to my library!'


if __name__ == '__main__':
    app.run()
