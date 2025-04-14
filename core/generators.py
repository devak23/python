from typing import Iterable, Any, Generator
from utils.logging_functions import logger


def read_numbers(n: int) -> Generator[int, Any, None]:
    for number in range(1, n + 1):
        yield number


def sqr(numbers: Iterable[int]) -> Generator[int | Any, Any, None]:
    for number in numbers:
        yield number ** 2


def filter_even(numbers: Iterable[int]) -> Generator[int | Any, Any, None]:
    for number in numbers:
        if number % 2 == 0:
            yield number


def main() -> None:
    limit = 100
    numbers = read_numbers(limit)
    even_numbers = filter_even(numbers)
    squared_evens = sqr(even_numbers)

    logger.info(f"sum of squares of even numbers from 1 to {limit} = {sum(squared_evens)}")



if __name__ == "__main__":
    main()