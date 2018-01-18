# Create a program that reads the length and width of a farmer’s field from the user in
# feet. Display the area of the field in acres. Hint: There are 43,560
# square feet in an acre.

import collections

Dimensions = collections.namedtuple('Dimensions', ['length', 'width'])
SQFT_PER_ACRE = 43560


def user_input():
    try:
        width = float(input('Enter the width of the field (in feet): '))
        length = float(input('Enter the length of the field (in feet): '))
        return Dimensions(length, width)
    except ValueError:
        return None
    except TypeError:
        return None


class FieldAreaCalculator:
    def main(self):
        dimensions = user_input()
        area = self.calculate_area(dimensions)
        print('Area of the fields (in acres) = ' +
              ('{:.2f}'.format(area) if area else 'None'))

    def calculate_area(self, dimensions):
        return (dimensions.width * dimensions.length / SQFT_PER_ACRE) if dimensions else None


if __name__ == '__main__':
    FieldAreaCalculator().main()
