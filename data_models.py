from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship

db = SQLAlchemy()


class Author(db.Model):
    __tablename__ = "authors"
    author_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    birth_date = Column(Date)
    date_of_death = Column(Date)

    def __repr__(self):
        return (f"Author(id={self.author_id}, name='{self.name}', birth_date=" 
                f"{self.birth_date}, date_of_death={self.date_of_death})")

    def __str__(self):
        return f"{self.name}"


class Book(db.Model):
    __tablename__ = "books"
    book_id = Column(Integer, primary_key=True, autoincrement=True)
    isbn = Column(String)
    title = Column(String)
    publication_year = Column(Integer)
    author_id = Column(Integer, ForeignKey('authors.author_id'),
                       nullable=False)
    author = relationship('Author', backref='books')

    def __repr__(self):
        return (f"Book(id={self.book_id}, isbn='{self.isbn}', title="
                f"'{self.title}', publication_year={self.publication_year}, "
                f"author_id={self.author_id})")

    def __str__(self):
        return f"{self.title} by {self.author.name}"