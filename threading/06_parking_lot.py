import uuid
from threading import Semaphore

AVAILABLE_SLOTS = 5


class Car:
    def __init__(self, owner: str) -> None:
        self.owner = owner
        self.token = None

    def assign_token(self, token):
        self.token = token

    def is_parked(self):
        return True if self.token else False

    def __repr__(self):
        return f"{self.owner}'s car"


class ParkingLot:
    def __init__(self):
        self.__slots: Semaphore = Semaphore(AVAILABLE_SLOTS)
        self.__space: dict = {}

    def assign_car(self, car: Car, token):
        self.__slots.acquire()
        self.__space[token] = car
        return True

    def release_car(self, token: str) -> Car | None:
        car_dict = {t: c for (t, c) in self.__space.items() if t == token}
        car_dict[token].assign_token(None)
        self.__slots.release()
        return car_dict[token]

    def has_empty_slots(self) -> bool:
        return len(self.__space) < AVAILABLE_SLOTS

    def is_slot_filled(self) -> bool:
        return len(self.__space) > 0

    def available_slots(self) -> int:
        return len(self.__space)

    def empty_slots(self) -> int:
        return AVAILABLE_SLOTS - self.available_slots()


class Vallet:
    def __init__(self, parking_lot):
        self.parking_lot = parking_lot

    def park(self, car: Car) -> (str, str):
        if self.parking_lot.has_empty_slots():
            token = uuid.uuid4()
            car.assign_token(token)
            self.parking_lot.assign_car(car, token)
            return token, car.owner
        else:
            return None, car.owner

    def unpark(self, token: str) -> Car | None:
        if not token:
            return None

        if self.parking_lot.is_slot_filled():
            return self.parking_lot.release_car(token)
        else:
            raise RuntimeError('No car is present in the slot')


def main() -> None:
    parking_lot = ParkingLot()

    cars = [Car('Suhas'), Car('KavitaK'), Car('KavitaY'), Car('Junaid'), Car('Saif'), Car('Avinash'),
            Car('Dinesh'), Car('Nimisha'), Car('Abrar'), Car('Nitin'),
            Car('Guru'), Car('Tejas'), Car('Purva'), Car('Chinmay'), Car('Mohita'), Car('Sana'),
            Car('Purva'), Car('Sahana')]

    vallet1 = Vallet(parking_lot)
    print(vallet1.park(cars[0]))
    print(vallet1.park(cars[1]))
    print(vallet1.park(cars[2]))
    print(vallet1.park(cars[3]))
    print(vallet1.park(cars[4]))
    print(vallet1.park(cars[5]))
    print(vallet1.park(cars[6]))
    print(f'Available slots: {parking_lot.available_slots()}, free slots: {parking_lot.empty_slots()}')

    print(vallet1.unpark(cars[0].token))
    print(vallet1.unpark(cars[1].token))
    print(vallet1.unpark(cars[2].token))
    print(vallet1.unpark(cars[3].token))
    print(vallet1.unpark(cars[4].token))
    print(vallet1.unpark(cars[5].token))
    print(vallet1.unpark(cars[6].token))

    print(f'Available slots: {parking_lot.available_slots()}, free slots: {parking_lot.empty_slots()}')


if __name__ == '__main__':
    main()
