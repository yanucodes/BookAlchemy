import os
from datetime import date
from flask import Flask, render_template, request
from data_models import db, Author

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(basedir, 'data', 'library.sqlite')
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{db_path}"
db.init_app(app)


@app.route('/add_author', methods=['GET', 'POST'])
def add_author():
    print_success_message = False
    if request.method == 'POST':
        name = request.form['name']
        birth_date = date.fromisoformat(request.form['birthdate'])
        date_of_death_input = request.form['date_of_death']
        date_of_death = (date.fromisoformat(date_of_death_input) if
            date_of_death_input else None)
        new_author = Author(name=name, birth_date=birth_date,
                            date_of_death=date_of_death)
        db.session.add(new_author)
        db.session.commit()
        print_success_message = True
    return render_template('add_author.html', print_success_message = print_success_message)


@app.route('/')
def welcome():  # put application's code here
    return 'Welcome to my library!'


if __name__ == '__main__':
    app.run()
