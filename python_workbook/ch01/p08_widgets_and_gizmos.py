# An online retailer sells two products: widgets and gizmos. Each widget weighs 75
# grams. Each gizmo weighs 112 grams. Write a program that reads the number of
# widgets and the number of gizmos in an order from the user. Then your program
# should compute and display the total weight of the order.

import collections

GIZMO_WEIGHT = 112
WIDGET_WEIGHT = 75

Cart = collections.namedtuple('Cart', ['widgets', 'gizmos'])


class WidgetsGizmos:
    def main(self):
        cart = self.user_input()
        weight = self.calculate_total_weight(cart)
        print('Total weight = {:.3f}'.format(weight))

    def user_input(self):
        try:
            widgets = int(input('How many widgets have you added in the order? -> '))
            gizmos = int(input('How many gizmos have you added in the order? -> '))
            return Cart(widgets, gizmos)
        except ValueError:
            print('Invalid input.')
            return None

    def calculate_total_weight(self, cart):
        if cart is None:
            return None

        if type(cart) is not Cart:
            raise TypeError('input is not of the correct type')

        if cart.gizmos is not None and cart.widgets is not None:
            if (cart.gizmos >= 0) and (cart.widgets >= 0):
                return (cart.gizmos * GIZMO_WEIGHT + cart.widgets * WIDGET_WEIGHT)

        return None


if __name__ == '__main__':
    WidgetsGizmos().main()
