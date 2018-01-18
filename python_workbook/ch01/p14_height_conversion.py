# Write a program that reads a number of feet from the user, followed by a number of inches. Once
# these values are read, your program should compute and display the equivalent number of centimeters.

import collections

HeightInFeet = collections.namedtuple("HeightInFeet", ["feet", "inches"])

ONE_FOOT_TO_INCH = 12
ONE_INCH_TO_CENTIMETER = 2.54

def user_input():
    try:
        print("Enter your height\n")
        feet = int(input("feet: "))
        inches = int(input("inches: "))
        return HeightInFeet(feet, inches)
    except ValueError:
        return None
    except TypeError:
        return None


class HeightConversion:

    def convert(self, height_in_feet):
        if height_in_feet is None:
            return None

        if not hasattr(height_in_feet, "feet") or not hasattr(height_in_feet, "inches") :
            raise TypeError("Incorrect object passed")

        feet = height_in_feet.feet if height_in_feet.feet else 0
        inches = height_in_feet.inches if height_in_feet.inches else 0

        if feet < 0 or inches < 0:
            raise ValueError("Feet and inches can't be negative")

        return (feet * ONE_FOOT_TO_INCH + inches) * ONE_INCH_TO_CENTIMETER


if __name__ == '__main__':
    hc = HeightConversion()
    height_in_cm = hc.convert(HeightInFeet(5, 2))
    print("HeightInFeet in centimeters = ", height_in_cm)