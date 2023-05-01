#!/usr/bin/python
# In this exercise, you will create a program that begins by reading a measurement
# in feet from the user. Then your program should display the equivalent distance in
# inches, yards and miles

class DistanceConverter:

    def __init__(self):
        self.__distance = -1

    def read_distance(self):
        try:
            self.__distance = float(input('Enter distance in feet: '))
        except ValueError:
            print('Invalid value entered')

    def convert_to_inches(self):
        return round(self.__distance * 12, 2)

    def convert_to_yards(self):
        """
        1 yard = 3 feet
        """
        return round(self.__distance * 0.33, 2)

    def convert_to_miles(self):
        """
        1 mile = 5,280 feet
        """
        return round(self.__distance * 0.000189394, 2)

    def convert(self):
        return self.__distance, self.convert_to_miles(), self.convert_to_yards(), self.convert_to_inches()


def main():
    ds = DistanceConverter()
    ds.read_distance()
    dist_feet, dist_miles, dist_yards, dist_inches = ds.convert()
    print(f'The distance in feet: {dist_feet}, in yards: {dist_yards}, in miles: {dist_miles}, in inches: {dist_inches} ')


if __name__ == '__main__':
    main()
