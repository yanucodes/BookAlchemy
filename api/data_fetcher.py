"""
Connect to openlibrary API to fetch data about authors and books.
"""

import logging
from datetime import date, datetime

import requests

logger = logging.getLogger(__name__)

API_AUTHORS = "https://openlibrary.org/search/authors.json"
API_BOOKS = "https://openlibrary.org/search.json"
OPENLIBRARY_DATE_FORMAT = "%d %B %Y"


def _parse_date(value: str) -> date | None:
    """
    Parse a date string returned by openlibrary API into a ``date`` object.

    Args:
        value: Date string in openlibrary format (e.g. "2 January 1920").

    Returns:
        Parsed ``date`` object. ``None`` if the value is missing or cannot be
        parsed.
    """
    if not value:
        return None
    try:
        return datetime.strptime(value, OPENLIBRARY_DATE_FORMAT).date()
    except (TypeError, ValueError):
        return None


def fetch_authors(name: str) -> dict:
    """
    Fetch information about an author with the name ``name``.

    Args:
        name: Search string passed to API.

    Returns:
        Dictionary with the information about the search results and a list of
        authors.

    Raises:
        ``requests.RequestException`` on API failure.
        ``TypeError`` in case of an unexpected API response.
    """
    result = requests.get(API_AUTHORS, params={"q": name}, timeout=30)
    result.raise_for_status()
    output_data = result.json()
    if not isinstance(output_data, dict):
        raise TypeError("Unexpected API response: not a dict.")
    output_data["authors"] = []
    author_docs = output_data.get("docs")
    if not isinstance(author_docs, list):
        raise TypeError("Unexpected API response: 'docs' is not found or is "
                        "not a list.")
    for author in author_docs:
        if not isinstance(author, dict):
            logger.warning(
                "Skipping non-dict entry in openlibrary 'docs': %r", author
            )
            continue
        author_name = author.get("name")
        if not author_name:
            logger.warning(
                "Skipping openlibrary author entry with no name: %r", author
            )
            continue
        birth_date = _parse_date(author.get("birth_date"))
        if birth_date is None:
            logger.warning(
                "Skipping openlibrary author entry with missing or "
                "unparseable birth date: %r", author
            )
            continue
        date_of_death = _parse_date(author.get("death_date"))
        new_author = {"name": author_name, "birth_date": birth_date,
                      "date_of_death": date_of_death}
        output_data["authors"].append(new_author)
    return output_data


def fetch_book_by_isbn(isbn: str) -> dict:
    """
    Fetch information about a book with the ISBN ``isbn``.

    Args:
        isbn: ISBN of the book.

    Returns:
        Dictionary with the information about the search results and a list of
        books under the ``books`` key. Each book is a dict with ``title``,
        ``author_name`` and ``publication_year``.

    Raises:
        ``requests.RequestException`` on API failure.
        ``TypeError`` in case of an unexpected API response (response is not
        a dict, ``docs`` is missing or not a list, or any entry in ``docs``
        is not a dict).
    """
    result = requests.get(API_BOOKS,
                          params={"isbn": isbn},
                          timeout=30)
    result.raise_for_status()
    output_data = result.json()
    if not isinstance(output_data, dict):
        raise TypeError("Unexpected API response: not a dict.")
    output_data["books"] = []
    book_docs = output_data.get("docs")
    if not isinstance(book_docs, list):
        raise TypeError("Unexpected API response: 'docs' is not found or is "
                        "not a list.")
    if len(book_docs) > 0:
        for book in book_docs:
            if not isinstance(book, dict):
                raise TypeError(
                    "Unexpected API response: book entry in 'docs' is not "
                    f"a dict: {book!r}"
                )
            title = book.get("title")
            if not title:
                logger.warning(
                    "Skipping openlibrary book entry with no title: %r", book
                )
                continue
            author_names = book.get("author_name") or []
            author_name = author_names[0] if author_names else None
            if not author_name:
                logger.warning(
                    "Skipping openlibrary book entry with no author: %r", book
                )
                continue
            publication_year = book.get("first_publish_year")
            if not isinstance(publication_year, int):
                logger.warning(
                    "Skipping openlibrary book entry with missing or "
                    "non-integer publication year: %r", book
                )
                continue
            new_book = {
                "title": title,
                "author_name": author_name,
                "publication_year": publication_year,
            }
            output_data["books"].append(new_book)
    return output_data
