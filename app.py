import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(basedir, 'data', 'library.sqlite')
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{db_path}"


@app.route('/')
def welcome():  # put application's code here
    return 'Welcome to my library!'


if __name__ == '__main__':
    app.run()
