import os
from datetime import date
from flask import Flask, render_template, request, redirect, url_for
from sqlalchemy import or_
from data_models import db, Author, Book

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(basedir, 'data', 'library.sqlite')
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{db_path}"
db.init_app(app)


@app.route('/book/<int:book_id>/delete', methods=['POST'])
def delete_book(book_id):
    book = Book.query.get_or_404(book_id)
    db.session.delete(book)
    db.session.commit()
    return redirect(url_for('home_page'))


@app.route('/add_author', methods=['GET', 'POST'])
def add_author():
    """
    Show the form to add a new author and handle submission.

    On GET: render the empty form.
    On POST: add author to the database and render the page in success state,
    exposing new_author_id for the template to optionally link to add_book.

    Returns:
        Rendered add_author.html template.
    """
    author_added = False
    new_author_id = None
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
        new_author_id = new_author.author_id
        author_added = True
    return render_template('add_author.html',
                           author_added=author_added,
                           new_author_id=new_author_id)


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
    preselected_author_id = request.args.get('author_id', type=int)
    return render_template('add_book.html',
                           print_success_message = print_success_message,
                           current_year=date.today().year,
                           authors=authors,
                           preselected_author_id=preselected_author_id)


@app.route('/books/search')
def search_book():
    keyword = request.args.get('keyword', False)
    if not keyword:
        return redirect(url_for('home_page'))
    pattern = f"%{keyword}%"
    query = Book.query.join(Author).filter(
        or_(
            Book.title.ilike(pattern),
            Author.name.ilike(pattern)
        )
    )
    books = query.all()
    return render_template('home.html', books=books)

@app.route('/')
def home_page():
    sort = request.args.get('sort', 'title')
    order = request.args.get('order', 'asc')

    sort_columns = {
        'title': Book.title,
        'author': Author.name,
        'year': Book.publication_year,
    }
    sort_column = sort_columns.get(sort, Book.title)
    sort_column = sort_column.desc() if order == 'desc' else sort_column.asc()

    query = Book.query
    if sort == 'author':
        query = query.join(Author)

    books = query.order_by(sort_column).all()
    return render_template('home.html', books=books, sort=sort, order=order)


if __name__ == '__main__':
    app.run()
