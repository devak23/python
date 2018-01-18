# Write a program that asks the user to enter the width and length of a room. Once
# the values have been read, your program should compute and display the area of the
# room. The length and the width will be entered as floating point numbers. Include
# units in your prompt and output message; either feet or meters, depending on which
# unit you are more comfortable working with.

import collections

Dimensions = collections.namedtuple('Dimensions', ['length', 'width'])


def user_input():
    try:
        width = float(input("Please enter the width of the room (in meters): "))
        length = float(input("Please enter the length of the room (in meters): "))
        return Dimensions(length, width)
    except ValueError:
        print('ValueError - Invalid input provided')
        return None
    except TypeError:
        print('TypeError - Invalid input provided')
        return None


class RoomAreaCalculator:
    def main(self):
        dimensions = user_input()
        area = self.calculate_area(dimensions)
        print('Area of the room (in meters) = ' + ('{:.2f}'.format(area) if area else 'None'))

    def calculate_area(self, dimensions):
        """ Important to note here: that calculate_area knows exactly what its expecting. When sending
        multiple variables to the function/method that performs operation, the parameters should be
        clearly defined. Here, the dimensions object (a named tuple) is defined to have a length
        """
        return dimensions.width * dimensions.length if dimensions else None


if __name__ == '__main__':
    RoomAreaCalculator().main()
