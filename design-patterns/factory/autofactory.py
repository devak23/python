from inspect import getmembers, isclass, isabstract
import autos


class AutoFactory(object):
    vehicles = {}  # Key = car model name, Value = class for the car

    def __init__(self):
        self.load_vehicles()

    def load_vehicles(self):
        classes = getmembers(autos, lambda m: isclass(m) and not isabstract(m))
        for name, _type in classes:
            if isclass(_type) and issubclass(_type, autos.AbsAuto):
                self.vehicles.update([[name, _type]])

    def create_instance(self, carname):
        if carname in self.vehicles:
            return self.vehicles[carname]()
        else:
            return autos.NullCar(carname)
