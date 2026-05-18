"""
Connect to openlibrary API to fetch data about a book
"""

from datetime import date, datetime
import requests


API_AUTHORS = "https://openlibrary.org/search/authors.json"
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


def _authors_default() -> dict:
    """
    Return default output for fetch_authors.
    """
    return {
        "numFound": 0,
        "start": 0,
        "numFoundExact": True,
        "docs": [],
    }


def fetch_authors(name: str) -> dict:
    """
    Fetch information about an author with the name ``name``.

    Args:
        name: Search string passed to API.

    Returns:
        Dictionary with the information about the search results and a list of
        authors. On failure, returns a dict shaped like an API response.
    """
    try:
        result = requests.get(API_AUTHORS,
                              params={"q": name},
                              timeout=30)
        authors_data = result.json()
        for author in authors_data.get("docs", []):
            author["birth_date"] = _parse_date(author.get("birth_date"))
            author["death_date"] = _parse_date(author.get("death_date"))
        return authors_data
    except (requests.RequestException, ValueError):
        return _authors_default()
