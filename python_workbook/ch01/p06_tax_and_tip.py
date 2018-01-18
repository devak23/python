# In many jurisdictions a small deposit is added to drink containers to encourage people
# to recycle them. In one particular jurisdiction, drink containers holding one liter or
# less have a $0.10 deposit, and drink containers holding more than one liter have a
# $0.25 deposit.
# Write a program that reads the number of containers of each size from the user.
# Your program should continue by computing and displaying the refund that will be
# received for returning those containers. Format the output so that it includes a dollar
# sign and always displays exactly two decimal places.

import collections

Surcharge = collections.namedtuple('Surcharge', ['tax', 'tip'])

TAX_PERCENT = 0.15
TIP_PERCENT = 0.12


def user_input():
    try:
        return float(input('Enter the cost of the meal: '))
    except ValueError:
        return None


class TaxesAndTips:
    def calculate_surcharge(self, cost):
        return Surcharge(cost * TAX_PERCENT, cost * TIP_PERCENT) if cost else None

    def main(self):
        cost = user_input()
        surcharge = self.calculate_surcharge(cost)
        if surcharge:
            print('The tax for the meal is {:.2f} and the tip is {:.2f}'.format(
                surcharge.tax, surcharge.tip))
            print('Total cost of the meal = {:.2f}'.format(
                cost + surcharge.tax + surcharge.tip))
        else:
            print('Error in program')


if __name__ == '__main__':
    TaxesAndTips().main()
