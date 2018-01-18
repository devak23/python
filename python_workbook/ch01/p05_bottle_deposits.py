# In many jurisdictions a small deposit is added to drink containers to encourage people
# to recycle them. In one particular jurisdiction, drink containers holding one liter or
# less have a $0.10 deposit, and drink containers holding more than one liter have a
# $0.25 deposit.
# Write a program that reads the number of containers of each size from the user.
# Your program should continue by computing and displaying the refund that will be
# received for returning those containers. Format the output so that it includes a dollar
# sign and always displays exactly two decimal places.

import collections

Bottles = collections.namedtuple(
    'Bottles', ['more_than_litre', 'a_litre_and_under'])
DEPOSIT_UNDER = 0.1
DEPOSIT_OVER = 0.25


def user_input():
    try:
        more_than_litre = int(input('How many more than a litre bottles do you have? '))
        a_litre_and_under = int(input('How many one litre or less bottles do you have? '))
        return Bottles(more_than_litre, a_litre_and_under)
    except ValueError:
        return None


class BottleDeposit:
    def compute_refund(self, bottles):
        return bottles.a_litre_and_under * DEPOSIT_UNDER + bottles.more_than_litre * DEPOSIT_OVER if bottles else None

    def main(self):
        bottles = user_input()
        refund = self.compute_refund(bottles)
        print('Refund on the containers returned = ' + ('${:.2f}'.format(refund) if refund else 'None'))


if __name__ == '__main__':
    BottleDeposit().main()
