# In the United States, fuel efficiency for vehicles is normally expressed in miles-per-
# gallon (MPG). In Canada, fuel efficiency is normally expressed in liters-per-hundred
# kilometers (L/100 km). Use your research skills to determine how to convert from
# MPG to L/100 km. Then create a program that reads a value from the user in American
# units and displays the equivalent fuel efficiency in Canadian units.

def user_input():
    choice = input("Would you like to enter mileage in miles per gallon (mpg) or kilometers per litre (kpl): ")
    if choice and (choice.lower() == 'mpg' or choice.lower() == 'kpl'):
        try:
            mileage = float(input("Enter the mileage: "))
            return mileage, choice.lower()
        except ValueError:
            return None
        except TypeError:
            return None

    print("Invalid choice. Program terminated")
    return None

class FuelEfficiency:
    MPG_TO_KPL_FACTOR = 0.425114
    KPL_TO_MPG_FACTOR = 2.35215

    def convert_to_miles_per_gallon(self, kmPerLitre):
        if kmPerLitre >= 0:
            return kmPerLitre * self.KPL_TO_MPG_FACTOR
        raise ValueError("Mileage cannot be negative")

    def convert_to_kilometers_per_litre(self, milesPerGallon):
        if milesPerGallon >= 0:
            return milesPerGallon * self.MPG_TO_KPL_FACTOR
        raise ValueError("Mileage cannot be negative")


if __name__ == '__main__':
    values = user_input()
    if values:
        mileage, input_miles = values
        fe = FuelEfficiency()
        if input_miles == 'mpg':
            print(mileage, "miles/gallon = ", fe.convert_to_kilometers_per_litre(mileage), "kms/litre")
        else:
            print(mileage, "kms/litre = ", fe.convert_to_miles_per_gallon(mileage), "miles/gallon")

