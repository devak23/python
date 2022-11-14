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
# to know/study it. However, for the lesser mortals like me, as long as the "GPS lady" correctly guides you from
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

import uuid
from concurrent.futures import ThreadPoolExecutor
from threading import Semaphore

AVAILABLE_SLOTS = 5


class Car:
    def __init__(self, employee: str) -> None:
        self.name = employee
        self._parked = False
        self.token = None

    def assign_token(self, token):
        self.token = token
        self._parked = True if token else False

    def is_parked(self):
        return self._parked


class ParkingLot:
    def __init__(self):
        self.__slots: Semaphore = Semaphore(AVAILABLE_SLOTS)
        self.__space: list = []

    def park(self, car: Car) -> (bool, str, str):
        if len(self.__space) < AVAILABLE_SLOTS:
            self.__slots.acquire()
            car.assign_token(uuid.uuid4())
            self.__space.append(car)
            return True, car.name, car.token
        else:
            return False, car.name, None

    def unpark(self, token: str) -> Car | None:
        if len(self.__space) > 0:
            self.__slots.release()
            slot = [s for s in self.__space if s.car.token == token]
            car = slot[0]
            car.assign_token(None)
            return car
        else:
            return None


def main() -> None:
    parking_lot = ParkingLot()

    cars = [Car('Suhas'), Car('KavitaK'), Car('KavitaY'), Car('Junaid'), Car('Saif'), Car('Avinash'),
            Car('Dinesh'), Car('Nimisha'), Car('Abrar'), Car('Nitin'),
            Car('Guru'), Car('Tejas'), Car('Purva'), Car('Chinmay'), Car('Mohita'), Car('Sana'),
            Car('Purva'), Car('Sahana')]

    with ThreadPoolExecutor(max_workers=4) as executor:
        result = executor.map(parking_lot.park, cars)

    for r in result:
        print(r)


if __name__ == '__main__':
    main()
