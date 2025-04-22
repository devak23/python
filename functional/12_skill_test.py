# Convert the following to a pure function that deals with immutable data
from typing import List


def verify(func):
    numbers = [1, 2, 3, 4, 5]
    incremented_numbers = func(numbers, 2)
    print(incremented_numbers)
    print(numbers)


def increment_elements_mutable(data: List[int], value: int) -> List[int]:
    for i in range(len(data)):
        data[i] += value

    return data

verify(increment_elements_mutable)


def increment_elements_immutable(data: List[int], value: int) -> List[int]:
    new_data = data[::-1]
    for i in range(len(new_data)):
        new_data[i] += value
    return new_data

verify(increment_elements_immutable)

def increment_elements_immutable2(data: List[int], value: int) -> List[int]:
    return [item + value for item in data]

verify(increment_elements_immutable2)