# So using a condition variable allows us to synchronize between two threads. But what if you had to synchronize across
# multiple threads? A semaphore comes to the rescue. "A sema-what??" you ask.. :). Yeah that stuff was new to me as well
# so I dug up a little. Apparently, semaphore was invented by a Dutch computer scientist - Edseger Dijkstra :(
# Not only his inventions are pain, but so is his name. I believe keeping English as the world's communication language
# till the foreseeable future, all the languages of the world including mine really ought to "normalize" the names that
# are easily "proun-ciable" (if there is such a word!). I mean c'mmon... Edseger Dijkstra? As an Indian myself, I
# pronounced his name as the sylables were introduced to me in kindergarten - "Ed-say-ger dee-jik-stra" but that doesn't
# have a nice ring to it. So I googled :| It turns out, the name is pronounced "ets-kar daa-eek-stra" with a very
# rounded D and T sounds (not sharp as in "dot" in english) :| Now, why does there have to be a j in his first name?
# Well, only the "dutchman" knows, but the point is Mr. Dijkstra being genius and all managed to make our lives
# miserable by investing his time into algorithms. This is a classic example of someone enjoying the cake and someone
# else footing the bill :( ... Anyways, Dijkstra's famous "Shortest Path Algorithm" is well known in the field of
# Computer Science. When I say "well known", I mean it is known to a lot of people, EXCEPT ME! But, depending on your
# career aspirations or your desire to socialize with the "masters of the universe" within the company, you might choose
# to know/study it. That said, for the lesser mortals like me, as long as the "GPS lady" correctly guides you from
# Sodawala Lane (Borivali) to Zhaveri Baazar (Kalbadevi), you are sorted.
#
# I have digressed... as I usually do. So, coming back, semaphore is a fancy word for "flag". This flag is basically a
# signal used for communicating with another thread. Ever seen railway folks wave a physical flag to an incoming/
# outgoing trains? THAT! my friend is a semaphore. If you google semaphore, that's what you will find in the images
# section.
#
# In the current context, the semaphore acts as a signal to the other threads about a certain condition. Let's try to
# understand this signalling by simulating a "parking lot problem" that we experience in everyday life. Again, this is
# a very standard interview question should any of you attempt in the near future ;). So we know there are specific # of
# slots in a parking lot. Any additional cars that come in will have to wait till somebody clears off their slot. That's
# what we will attempt to build using semaphores. Let's see how.
import time
import uuid
from threading import Semaphore, Thread, BoundedSemaphore

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
        self.__slots: Semaphore = BoundedSemaphore(AVAILABLE_SLOTS)
        self.__space: dict = {}

    def assign_car(self, car: Car, token):
        self.__slots.acquire()
        self.__space[token] = car
        return True

    def release_car(self, token: str):
        self.__slots.release()
        car_dict = {t: c for (t, c) in self.__space.items() if t == token}

        car_dict[token].assign_token(None)
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
        self._continue = True

    def park(self, car: Car) -> (str, str):
        if self.parking_lot.has_empty_slots():
            token = uuid.uuid4()
            car.assign_token(token)
            self.parking_lot.assign_car(car, token)
            return token, car.owner
        else:
            return None, car.owner

    def unpark(self, token: str) -> Car:
        if self.parking_lot.is_slot_filled():
            return self.parking_lot.release_car(token)
        else:
            raise RuntimeError('No car is present in the slot')

    def park_cars(self, unparked_cars: list, parked_cars: list):
        while self._continue and len(unparked_cars) > 0:
            for c in unparked_cars:
                self.park(c)
                parked_cars.append(c)
                unparked_cars.remove(c)
                time.sleep(1)
                print(f"{c.owner}'s car is parked")

    def unpark_cars(self, parked_cars: list):
        while self._continue and len(parked_cars) > 0:
            for c in parked_cars:
                self.unpark(c.token)
                time.sleep(5)
                parked_cars.remove(c)
                print(f"-----{c.owner}'s car is vacated")


def main() -> None:
    parking_lot = ParkingLot()

    cars = [Car('Suhas'), Car('Kavita K'), Car('Kavita Y'), Car('Junaid'), Car('Saif'), Car('Avinash'),
            Car('Dinesh'), Car('Nimisha'), Car('Abrar'), Car('Nitin'),
            Car('Guru'), Car('Tejas'), Car('Purva'), Car('Chinmay'), Car('Mohita'), Car('Sana'),
            Car('Purva'), Car('Sahana')]

    unparked_cars = [] + cars
    parked_cars = []

    vallet1 = Vallet(parking_lot)
    vallet2 = Vallet(parking_lot)

    tvallet1 = Thread(target=vallet1.park_cars, args=(unparked_cars, parked_cars))
    tvallet2 = Thread(target=vallet2.unpark_cars, args=(unparked_cars, parked_cars,))

    tvallet1.start()
    # time.sleep(10)
    # tvallet2.start()


if __name__ == '__main__':
    main()
