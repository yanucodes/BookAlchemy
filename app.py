import os
from datetime import date
from flask import Flask, render_template, request
from data_models import db, Author, Book

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


@app.route('/add_book', methods=['GET', 'POST'])
def add_book():
    print_success_message = False
    if request.method == 'POST':
        isbn = request.form['isbn']
        title = request.form['title']
        publication_year = int(request.form['publication_year'])
        author_id = int(request.form['author_id'])
        new_book = Book(isbn=isbn, title=title,
                        publication_year=publication_year, author_id=author_id)
        db.session.add(new_book)
        db.session.commit()
        print_success_message = True
    authors = Author.query.order_by(Author.name).all()
    print(authors)
    return render_template('add_book.html',
                           print_success_message = print_success_message,
                           current_year=date.today().year,
                           authors=authors)


@app.route('/')
def welcome():  # put application's code here
    return 'Welcome to my library!'


if __name__ == '__main__':
    app.run()
