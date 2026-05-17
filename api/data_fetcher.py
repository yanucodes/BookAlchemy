"""
Connect to openlibrary API to fetch data about a book
"""

import requests


API_AUTHORS = "https://openlibrary.org/search/authors.json"


def _authors_default() -> dict:
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
        return result.json()
    except (requests.RequestException, ValueError):
        return _authors_default()
