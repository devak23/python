p = lambda *anything: print(*anything)

numbers = range(1, 11)
evens = filter(lambda x: x % 2 == 0 and x > 5, numbers)  # this also returns us a generator!
p(f"evens = {evens}")

words = ["apple", "banana", "cherry", "date", "eggplant", "fig", "grape", "watermelon", "orange"]
five_letter_word = filter(lambda x: len(x) == 5, words)
p(f"five_letter_word = {five_letter_word}")

# multiple conditions in filter
books = [
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

def is_genre(book, genre):
    return book["genre"].lower() == genre.lower()


def has_min_rating(book: dict, min_rating: float):
    return book["rating"] >= min_rating


def is_alphabet_before(book, letter):
    return book["title"][0].lower() < letter.lower()


filtered_books_gen = filter(lambda book:
                            is_genre(book, "fantasy") and
                            has_min_rating(book, 4.0) and
                            is_alphabet_before(book, 'M'), books)

p("filtering 1: ", list(filtered_books_gen)) # production ready code will be found in 21_filter.py

# another way is to chain the lambda functions like so
with_genre = filter(lambda book: book['genre'].lower() == 'fantasy', books)
with_rating = filter(lambda book: book['rating'] >= 4.0, with_genre)
with_letter = filter(lambda book: book['title'][0].lower() < 'm', with_rating)
p('filtering 2:', list(with_letter))

