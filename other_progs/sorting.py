#!/usr/bin/python

# An implementation of the quick sort algorithm

from enum import Enum


class Order(Enum):
    ASCENDING = 1
    DESCENDING = 2


def quicksort(collection, order):
    "Quicksort over a list-like sequence"
    if len(collection) == 0:
        return collection

    pivot = collection[0]
    small = quicksort([f for f in collection if f < pivot], order)
    large = quicksort([f for f in collection if f > pivot], order)

    return (large + [pivot] + small) if order == Order.DESCENDING else (small + [pivot] + large)


if __name__ == '__main__':
    colleagues = ['Guru', 'Avinash', 'Ashwani', 'Tejas', 'Abhay', 'Srini', 'Rakshapal', 'Suhas', 'Lokesh']
    sorted_colleagues = quicksort(colleagues, Order.ASCENDING)
    print(sorted_colleagues)
