from typing import Generator, Iterable

lazy_squares1 = (x * x for x in range(10))
eager_squares1 = [x * x for x in range(10)]


def lazy_evens(n: int) -> Generator[int]:
    for i in range(n):
        if i % 2 == 0:
            yield i

gen_func = lazy_evens(10)

print(next(gen_func))
print(next(gen_func))
print(next(gen_func))


# note the use of the Iterable input to the function which allows a generator to be passed on to this function
def lazy_squares(n: Iterable) -> Generator[int]:
    for i in n:
        yield i ** 2

squared_evens1 = lazy_squares(lazy_evens(10))
print(next(squared_evens1))
print(next(squared_evens1))

numbers = [10, 20, 30]
# note here we are invoking the same lazy_squares with a list of numbers
lazy_numbers = lazy_squares(numbers)

print(next(lazy_numbers))
print(next(lazy_numbers))
print(next(lazy_numbers))