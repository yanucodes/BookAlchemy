import os
from flask import Flask
from data_models import db

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(basedir, 'data', 'library.sqlite')
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{db_path}"
db.init_app(app)


@app.route('/')
def welcome():  # put application's code here
    return 'Welcome to my library!'


if __name__ == '__main__':
    app.run()
