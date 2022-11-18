# So using a condition variable allows us to synchronize between two threads. But what if you had to synchronize across
# multiple threads? Like how would you allow a "controlled access" to a certain number of threads? Any guesses? Well a
# semaphore comes to the rescue. "A sema-what??" you ask.. :). Yeah that stuff was new to me as well so I dug up a
# little. Apparently, semaphore was invented by a Dutch computer scientist - Edseger Dijkstra :( Not only his inventions
# are pain, but so is his name! I believe keeping English as the world's communication language for a foreseeable future
# all the languages of the world including mine really ought to "normalize" the names that are easily "proun-ciable"
# (if there is such a word!). I mean c'mmon... Edseger Dijkstra? As an Indian myself, I pronounced his name as the
# sylables were introduced to me in kindergarten - "Ed-say-ger dee-jik-stra". I know I inserted the 'i' there but I
# couldn't really pronounce jk together without making an i sound... try it and you will know what I mean. Anyways, my
# way of pronounciation of Mr. Dijkstra doesn't have a nice ring to it. So I googled :| It turns out, the name is
# pronounced "ets-kar daa-eek-stra" with a very rounded D and T sounds (not sharp as in "dot" in english) :| Now, why
# does there have to be a j in his first name? Well, only the "dutchman" knows, but the point is Mr. Dijkstra being
# genius and all managed to make our lives miserable by investing his time into algorithms. This is a classic case of
# someone enjoying the cake and someone else footing the bill :( ... Anyways, Dijkstra's famous "Shortest Path
# Algorithm" is well known in the field of Computer Science. When I say "well known", I mean it is known to a lot many
# people, EXCEPT ME! :| Now, depending on your career aspirations or your desire to socialize with the "tech gurus"
# within the company, you might choose to know/study it. For the rest of lesser mortals like me, as long as the
# "GPS lady" correctly guides you from Sodawala Lane (Borivali) to Zhaveri Baazar (Kalbadevi), you are sorted :D
#
# I have digressed... as I usually do :|. So, coming back, semaphore is a fancy word for "flag". This flag is basically a
# signal used for communicating with another thread. Ever seen railway folks wave a physical flag to an incoming/
# outgoing trains? THAT! my friend is a semaphore. In the software parlance, a semaphore will keep a track of how many
# threads "acquire" it and how many "release" it. Typically, you initialize a Semaphore by a count and then keep on
# "acquiring it" after a certain point the acquire call will not get you the lock and the method/behavior is protected
# and that is how synchronization is achieved.
#
# In the current context, the semaphore acts as a signal to the other threads about a certain condition. Let's try to
# understand this signalling by simulating a "parking lot problem" that we experience in everyday life. Again, this is
# a very standard interview question should any of you attempt in the near future ;). So we know there are specific # of
# slots in a parking lot. Any additional cars that come in will have to wait till somebody clears off their slot. That's
# what we will attempt to build using semaphores. Let's see how.

import uuid
from threading import Semaphore

AVAILABLE_SLOTS = 5


class Car:
    """
    Let's define a car with an owner. When the car is parked, you (the car owner) will get a token. But instead of
    creating another class called the Owner and trying to model it correctly, I took a shortcut and placed the token
    here instead. :( Not something you should do in a real life.
    """
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

    print("Lets start parking the cars...")
    print(vallet1.park(cars[0]))
    print(vallet1.park(cars[1]))
    print(vallet1.park(cars[2]))
    print(vallet1.park(cars[3]))
    print(vallet1.park(cars[4]))
    print(vallet1.park(cars[5]))
    print(vallet1.park(cars[6]))
    print(vallet1.park(cars[7]))
    print(vallet1.park(cars[8]))
    print(f'Available slots: {parking_lot.available_slots()}, free slots: {parking_lot.empty_slots()}')

    print("Lets start 'unparking' the cars...")
    print(f'{vallet1.unpark(cars[0].token)} is unparked')
    print(f'{vallet1.unpark(cars[1].token)} is unparked')
    print(f'{vallet1.unpark(cars[2].token)} is unparked')
    print(f'{vallet1.unpark(cars[3].token)} is unparked')
    print(f'{vallet1.unpark(cars[4].token)} is unparked')
    print(f'{vallet1.unpark(cars[5].token)} is unparked')
    print(f'{vallet1.unpark(cars[6].token)} is unparked')
    print(f'{vallet1.unpark(cars[7].token)} is unparked')
    print(f'{vallet1.unpark(cars[8].token)} is unparked')

    print(f'Available slots: {parking_lot.available_slots()}, free slots: {parking_lot.empty_slots()}')


if __name__ == '__main__':
    main()
