"""Default imports from api module"""

from api.data_fetcher import fetch_authors, fetch_book_by_isbn

__all__ = ["fetch_authors", "fetch_book_by_isbn"]
