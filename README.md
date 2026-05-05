# BookAlchemy Web App

A Flask powered Web App to organize your library. With this app you can add books in your database through a web interface.

## Getting Started

### Prerequisites

- Python 3.9+

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/yanucodes/BookAlchemy.git
cd BookAlchemy

# 2. Install dependencies
pip install -r requirements.txt
```

Create `.flaskenv` file containing set up for the local flask server.
```
echo "FLASK_RUN_HOST=127.0.0.1" > .flaskenv
echo "FLASK_RUN_PORT=5000" >> .flaskenv
```
**macOS users:** Port 5000 is used by AirPlay Receiver. Replace 5000 with 5001 
in the second command (or disable AirPlay Receiver in System Settings).

## Usage

```bash
flask run
```

## Database setup

An example database is included in the package, you can delete it and create an empty one using included python script:
```bash
python setup.py
```

## Routes

| Method      | Path                      | Description                  |
|-------------|---------------------------|------------------------------|
| GET         | `/`                       | List all books               |
| GET, POST   | `/add_author`             | Add new author               |
| GET, POST   | `/add_book`               | Add new book                 |
| POST        | `/book/<book_id>/delete`  | Delete a book                |

The home page will display all books in your library. You can also add new book (if you don't find an author in the dropdown menu, add it with using the link in the form for adding a new book), delete existing books, search for a book with keyword. 

Enjoy!
