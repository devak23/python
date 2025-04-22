from typing import List


def add_element(data: List[int], element: int) -> List[int]:
    data.append(element)
    return data

ages = [21, 25, 23, 22]

new_ages = add_element(ages, 24)
print(new_ages)
print(ages)

def add_element_immutable(data: List[int], element: int) -> List[int]:
    return data + [element]


stock_prices = [101, 110, 120, 125]

new_stock_prices = add_element_immutable(stock_prices, 123)
print(new_stock_prices)
print(stock_prices)