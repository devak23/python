# multiple conditions in filter - Production ready code
from typing import Dict, List

BOOKS = [
    {"title": "The Hobbit", "genre": "Fantasy", "rating": 4.7},
    {"title": "Dune", "genre": "Sci-Fi", "rating": 4.5},
    {"title": "To Kill a Mocking bird", "genre": "Classics", "rating": 4.9},
    {"title": "Eragon", "genre": "Fantasy", "rating": 4.1},
    {"title": "The Catcher in the rye", "genre": "Classics", "rating": 3.8},
    {"title": "Mistborn", "genre": "Fantasy", "rating": 4.7},
]


# Selection criteria
# genre must be fantasy
# rating must be 4.5
# title must come before M

def is_valid(book: Dict) -> bool:
    """
    Validates if a book and its members are of the correct types
    """

    if not isinstance(book, dict):
        return False

    required_keys = ['title', 'genre', 'rating']
    for key in required_keys:
        if key not in book or book[key] is None:
            return False

    if not isinstance(book['title'], str) or not book['title'].strip():
        return False

    if not isinstance(book['genre'], str) or not book['genre'].strip():
        return False

    if not isinstance(book['rating'], float) or book['rating'] < 0:
        return False

    return True


def is_genre(book: Dict, genre: str) -> bool:
    """
    Checks if the given book belongs to the given genre
    """
    return book.get('genre').strip().lower() == genre.lower()


def has_min_rating(book: Dict, min_rating: float) -> bool:
    """
    Checks if the given book has a rating greater than or equal to the given min_rating
    """

    try:
        rating = float(book.get('rating', 0))
        return rating >= min_rating
    except (ValueError, TypeError):
        return False

def is_alphabet_before(book: Dict, alphabet: str) -> bool:
    """
    Checks if the title of the book starts with an alphabet that comes before the given alphabet
    """
    return book.get('title').lower() < alphabet.lower()


def filter_books(books: List[Dict], genre: str, letter: str, rating: float) -> List[Dict]:
    """
    returns a list of books that are filtered with the given parameters
    """
    if not isinstance(books, list):
        raise ValueError("Books should be a list of dictionaries")

    fb_gen = filter(lambda book:
                    is_valid(book) and
                    is_genre(book, genre) and
                    has_min_rating(book, rating) and
                    is_alphabet_before(book, letter), books)
    return list(fb_gen)


def main() -> None:
    filtered_books = filter_books(BOOKS, "fantasy", letter="f", rating=4.0)
    print(filtered_books)


if __name__ == '__main__':
    main()