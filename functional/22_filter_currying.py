from typing import Dict, Callable, List, Iterable

p = lambda *anything: print(*anything)

books = [
    {"title": "The Hobbit", "genre": "Fantasy", "rating": 4.7},
    {"title": "Dune", "genre": "Sci-Fi", "rating": 4.5},
    {"title": "To Kill a Mocking bird", "genre": "Classics", "rating": 4.9},
    {"title": "Eragon", "genre": "Fantasy", "rating": 4.1},
    {"title": "The Catcher in the rye", "genre": "Classics", "rating": 3.8},
    {"title": "Mistborn", "genre": "Fantasy", "rating": 4.7},
]


def with_genre(genre: str) -> Callable[[Dict], bool]:
    def _inner_genre(book: Dict) -> bool:
        return book.get('genre').strip().lower() == genre.strip().lower()

    return _inner_genre


def with_rating(min_rating: float) -> Callable[[Dict], bool]:
    def _inner_rating(book: Dict) -> bool:
        return float(book.get('rating')) >= min_rating

    return _inner_rating


def with_letter_lower(letter: str) -> Callable[[Dict], bool]:
    def _inner_letter_lower(book: Dict) -> bool:
        return book.get('title').strip().lower()[0] < letter.lower()

    return _inner_letter_lower


def filter_books(books: List[Dict], genre: str, rating: float, letter: str) -> Iterable[Dict]:
    filter_genre = with_genre(genre)
    filter_rating = with_rating(rating)
    filter_title = with_letter_lower(letter)

    return filter(lambda book:
                  filter_genre(book) and
                  filter_rating(book) and
                  filter_title(book), books)


if __name__ == '__main__':
    filtered_books_generator = filter_books(books, genre="fantasy", rating=4.0, letter="F")
    p(list(filtered_books_generator))