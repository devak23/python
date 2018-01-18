# The surface of the Earth is curved, and the distance between degrees of longitude
# varies with latitude. As a result, finding the distance between two points on the surface
# of the Earth is more complicated than simply using the Pythagorean theorem.
# Let (t1 , g1 ) and (t2 , g2 ) be the latitude and longitude of two points on the Earth’s
# surface. The distance between these points, following the surface of the Earth, in
# kilometers is:
#
# distance = 6371.01 × arccos(sin(t1) × sin(t2) + cos(t1) × cos(t2) × cos(g1 − g2))
#
# The value 6371.01 is the average radius of the Earth in kilometers.
#
# Create a program that allows the user to enter the latitude and longitude of two
# points on the Earth in degrees. Your program should display the distance between
# the points, following the surface of the earth, in kilometers.
import collections
from math import sin, cos, acos

LatLong = collections.namedtuple("LatLong", ["latitude", "longitude"])


def user_input():
    try :
        lat1 = float(input("Enter the latitude of location 1: "))
        long1 = float(input("Enter the longitude of location 1: "))

        lat2 = float(input("Enter the latitude of location2: "))
        long2 = float(input("Enter the longitude of location2: "))

        return (LatLong(lat1, long1), LatLong(lat2, long2))
    except ValueError:
        return None
    except TypeError:
        return None

class PointsOnEarth:
    def calculate_distance(self, loc1, loc2):
        if loc1 is None or loc2 is None:
            raise ValueError("One of the input locations is Null")

        if loc1.latitude is None \
            or loc1.longitude is None \
            or loc2.latitude is None \
            or loc2.longitude is None:
            raise ValueError("either of latitude and longitude cannot be null")


        return 6371.01 * acos(
            sin(loc1.latitude) * sin(loc2.latitude)
            + cos(loc1.latitude) * cos(loc2.latitude) * cos(loc1.longitude - loc2.longitude)
        )

if __name__ == '__main__':
    values = user_input()
    if values:
        loc1, loc2 = values
        poe = PointsOnEarth()
        print("Distance between the two places (in kms) is: ", poe.calculate_distance(loc1, loc2))
    else:
        print("Invalid input encountered! Terminating program")
