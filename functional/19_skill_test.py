# You have been provided with sales inventory of a retail store. Create a comprehensive report that showcases items,
# their price, colors. Further enhance this data with new features and ensure its integrity
import json
from pprint import pprint
from typing import Tuple, Dict

# Attributes:
# items
# prices
# colors
# discounts

# Use the zip function to combine items, prices, colors and discounts into a list of tuples. Each tuple should represent
# a product in store.

# Ensure that length of items, prices, colors and discounts are equal using strict mode of zip. If not, raise relevant error

# For each product, calculate the discounted price and append it to the tuple. Formula: price = price(1-discount/100) rounded
# to 2 decimal places


# build a report where the keys are item names and value is another dictionary containing price, colors and discounted price

p = lambda *anything: print(*anything)

items = ['Shirt', 'Pants', 'Shoes', 'Hat']
prices = [19.95, 29.99, 47.95, 9.99]
colors = ['Red', 'Blue', None, 'Black']
discounts = [10, 0, 20, 5]

def calc_discounted_price(price: float, discount: int) -> float:
    if discount and discount > 0 and price:
        return round(price * (1 - (discount / 100)),2)
    else:
        return price


def generate_report_traditional(zipped_items: zip) -> dict:
    rep = {}
    for item, price, color, discount in zipped_items:
        rep[item] = {'color': color, 'original price': price,
                        'discounted price': calc_discounted_price(price, discount), 'discount': discount}

    return rep


def generate_report_idiomatic(zipped_items: zip) -> dict:
    return {
        item: {
            'Price': price,
            'Color': color,
            'Discounted Price': calc_discounted_price(price, discount),
            'Discount': discount
        }
        for item, price, color, discount in zipped_items
    }

try :
    inventory1 = zip(items, prices, colors, discounts, strict=True)
    inventory2 = zip(items, prices, colors, discounts, strict=True)
    # [('Shirt', 20.0, 'Red', 10), ('Pants', 30.0, 'Blue', 0), ('Shoes', 50.0, None, 20), ('Hat', 10.0, 'Black', 5)]

    report = generate_report_traditional(inventory2)
    pprint(report)


    report = generate_report_idiomatic(inventory1)
    with open("report.json", "w") as f:
        json.dump(report, f, indent=4)

except ValueError as ve:
    p("All the items need to have the same length")



