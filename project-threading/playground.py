from collections import OrderedDict
from typing import Dict, Any


def func(a: int) -> int:
    return a * 2

def func2(a: float) -> float:
    return a * 2

def func3(a: int | float) -> int | float:
    return a * 2

result = func(1)
print(result)

print(func3(2.0))
print(func3(2))


import sys

age1 = 46
age2 = 464646464646464646464646464646464646464646464646
print(f"Integer size age1 = {sys.getsizeof(age1)} bytes and age2 = {sys.getsizeof(age2)} bytes")


my_fraction = 0.3
print(f"Float size my_fraction = {sys.getsizeof(my_fraction)} bytes")
print(f"my_fraction = {my_fraction}")
new_float = 1/10 + 1/10 + 1/10
print(f"new_float = {new_float}")

import math
def float_is_equal(x,y):
    epsilon = 1e-15
    difference = math.fabs(x - y)
    return difference < epsilon

print(float_is_equal(my_fraction, new_float))
print(math.isclose(my_fraction, new_float, abs_tol=1e-15, rel_tol=1e-09))


print(f"size of True = {sys.getsizeof(True)} bytes") # 28 bytes
print(f"size of False = {sys.getsizeof(False)} bytes") # 28 bytes
print(issubclass(bool, int)) # true

my_bool = True
my_int = 1
print(my_bool == my_int) # true
print(my_bool is my_int) # false

def guessing_game(guess: int) -> None:
    match guess:
        case guess if guess < 0:
            print(f"guess is not valid!")
        case 2:
            print(f"{guess} is close!")
        case 4:
            print(f"{guess} - You Won!")
        case 7 | 8 | 9:
            print(f"{guess} close!")
        case _:
            print(f"{guess} is not a correct value!")

guessing_game(4)


my_list = [i for i in range(10) if i < 3]
print(my_list) # [0, 1, 2] - filtering

my_list2 = [i if i < 3 else -1 for i in range(10)]
print(my_list2) # [0, 1, 2, -1, -1, -1, -1, -1, -1, -1] - will always have 10 elements

def memory_address(element: Any) -> str:
    return hex(id(element))

def print_dict(dct: Dict[str, Any]) -> None:
    print(f"Dict address: {memory_address(dct)}")
    for key, value in dct.items():
        print(f"{key} = {memory_address(value)}")

my_dict1 = {'key' + str(i): i**2 for i in range(10)}
print_dict(my_dict1)

# ---------------------------------------------------------------
import requests
from lxml import html
headers = {}
headers['User-Agent'] = "Mozilla/6.0 (X11; Ubuntu; Linux i586; rv:49.0) Gecko/20200202 Firefox/49.0"
r = requests.get('http://finance.yahoo.com/quote/DLR?p=DLR', headers=headers)
page_contents = html.fromstring(r.content)
# print(page_contents.xpath('//*[@id="nimbus-app"]/section/section/section/article/section[1]/div[1]/div/div[1]/section/h1')[0].text)
price_element = page_contents.xpath(
    '//*[@id="nimbus-app"]/section/section/section/article/section[1]/div[2]/div[1]/section/div/section[1]/div[1]/div[1]/span')
if price_element:
    print(price_element[0].text)
else:
    print([])
# ---------------------------------------------------------------