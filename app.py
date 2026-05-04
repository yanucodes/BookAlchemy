"""Web application for displaying books in the database, adding new books,
or deleting old ones."""
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
    """
    Delete the book with the given ID from the database.

    Args:
        book_id: ID of the book to delete.

    Returns:
        Redirect to the home page.
    """
    book = Book.query.get_or_404(book_id)
    db.session.delete(book)
    db.session.commit()
    return redirect(url_for('home_page'))


@app.route('/add_author', methods=['GET', 'POST'])
def add_author():
    """
    Show the form to add a new author and handle submission.

    On GET: render the empty form.
    On POST: add the author to the database and render the page in success
    state,
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
    """
    Show the form to add a new book and handle submission.

    On GET: render the empty form. If author_id is passed, preselect that
    author in the author dropdown.
    On POST: add book to the database and render the page in success state.

    Returns:
        Rendered add_book.html template.
    """
    book_added = False
    if request.method == 'POST':
        isbn = request.form['isbn']
        title = request.form['title']
        publication_year = int(request.form['publication_year'])
        author_id = int(request.form['author_id'])
        new_book = Book(isbn=isbn, title=title,
                        publication_year=publication_year, author_id=author_id)
        db.session.add(new_book)
        db.session.commit()
        book_added = True
    authors = Author.query.order_by(Author.name).all()
    preselected_author_id = request.args.get('author_id', type=int)
    return render_template('add_book.html',
                           book_added=book_added,
                           current_year=date.today().year,
                           authors=authors,
                           preselected_author_id=preselected_author_id)


def sort_books(query, sort: str = 'title', descending: bool = False):
    """
    Sort the books in the given query by the selected column.

    Args:
        query: a Book query to sort.
        sort: sorting column.
        descending: if true, sort books in descending order.

    Returns:
        Query with books sorted by the selected column.
    """
    sort_columns = {
        'title': Book.title,
        'author': Author.name,
        'year': Book.publication_year,
    }
    if sort == 'author':
        query = query.join(Author)
    sort_column = sort_columns.get(sort, Book.title)
    sort_column = sort_column.desc() if descending else sort_column.asc()
    return query.order_by(sort_column)


def filter_books_by_keyword(query, keyword):
    """
    Filter books by keyword presence in the title or in the author's name.

    Args:
        query: a Book query to filter.
        keyword: keyword to search for.

    Returns:
        Filtered query containing only books with the keyword in either the
        title or the author's name.
    """
    pattern = f"%{keyword}%"
    return query.filter(
        or_(
            Book.title.ilike(pattern),
            Book.author.has(Author.name.ilike(pattern))
        )
    )


@app.route('/')
def home_page():
    """
    Render the home page with a list of books in the database.

    Returns:
        Rendered home.html template with books sorted and filtered according
        to the passed parameters.
    """
    sort = request.args.get('sort', 'title')
    order = request.args.get('order', 'asc')
    keyword = request.args.get('keyword', '')
    query = Book.query
    if keyword:
        query = filter_books_by_keyword(query, keyword)
    query = sort_books(query, sort=sort, descending=order == 'desc')
    books = query.all()
    return render_template('home.html', books=books, sort=sort, order=order,
                           keyword=keyword)


if __name__ == '__main__':
    app.run()
