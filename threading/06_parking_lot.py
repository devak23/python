# So using a condition variable allows us to synchronize between two threads. But what if you had to synchronize across
# multiple threads? Like how would you allow a "controlled access" to a certain number of threads? Any guesses? Well a
# semaphore comes to the rescue. Apparently, semaphore was invented by a Dutch computer scientist - Edseger Dijkstra :(
# Not only his inventions are pain, but so is his name! I believe keeping English as the world's communication language
# for a foreseeable future all the languages of the world including mine really ought to "normalize" the names that
# are easily "proun-ciable" (if there is such a word!). I mean c'mmon... Edseger Dijkstra? As an Indian myself, I
# pronounced his name as the sylables were introduced to me in kindergarten - "Ed-say-ger dee-jik-stra". I know I
# inserted the 'i' there, but I couldn't really pronounce jk together without making an "e" sound. I know ... lame! :(
# Anyways, my way of pronounciation of that name doesn't have a nice ring to it. So I googled :| It turns out, the name
# is pronounced "ets-kar daa-eek-stra" with a very rounded D and T sounds (not sharp as in "dot" in english) :| Now, why
# does there have to be a j in his first name? :| Well, only the "dutchman" knows, but the point is Mr. Dijkstra being
# genius and all managed to get us into trouble by investing his time into algorithms. This is a classic case of
# someone enjoying the cake and someone else footing the bill :( ... Anyways, Dijkstra's famous "Shortest Path
# Algorithm" is well known in the field of Computer Science. When I say "well known", I mean it is known to a lot many
# people, EXCEPT ME! :| Now, depending on your career aspirations or your desire to socialize with the "tech gurus"
# within the company, you might choose to know/study it. For the rest of lesser mortals like me, as long as the
# "GPS lady" correctly guides you from Sodawala Lane (Borivali) to Zhaveri Baazar (Kalbadevi), you are sorted ;)
#
# I have digressed... as I usually do :|. So, coming back, semaphore is a fancy word for "flag". This flag is basically a
# signal used for communicating with another thread. Ever seen railway folks wave a physical flag to an incoming/
# outgoing trains? THAT! my friend is a real life semaphore. In the software universe, a semaphore will allow communication
# between specific # of threads and enable concurrency. You could achieve the same goal with locks and a counter, but
# why re-invent the wheel when a Semaphore is handy? Typically, you initialize a Semaphore by a count and then keep on
# "acquiring it". After a certain point the acquire call will not get you the lock and the method/behavior is protected
#
# Let's try to understand this signalling by simulating a "parking lot problem" that we experience in everyday life. A
# very standard interview question ;). So we know there are specific # of slots in a parking lot. Any additional cars
# that come in will have to wait till somebody clears off their slot. That's what we will attempt to build using
# semaphores. Let's get into it.

import uuid
from threading import Semaphore
from typing import Tuple
from uuid import UUID

AVAILABLE_SLOTS = 5


class Car:
    """
    Let's define a car with an owner. When the car is parked, you (the car owner) will get a token. But instead of
    creating another class called the Owner and trying to model it correctly, I took a shortcut and placed the token
    here instead. :( Not something you should do in a real life. This is a toy example only for demonstration purpose
    """
    def __init__(self, owner: str) -> None:
        self.owner = owner
        self.token = None

    def assign_token(self, token) -> None:
        """
        A token gets assigned to you (car in this case) when the car is parked.
        """
        self.token = token

    def is_parked(self) -> bool:
        return True if self.token else False

    def __repr__(self) -> str: # toString() method
        return f"{self.owner}'s car"


class ParkingLot:
    """
    A parking lot will define slots which will be our Semaphore that will control how many cars can come in. It also
    has a physical space initialized by a dictionary object (Map in Java)
    """
    def __init__(self) -> None:
        self.__slots: Semaphore = Semaphore(AVAILABLE_SLOTS)
        self.__space: dict = {} # the nice thing is the dict looks like a JSON in python :) All you got to do to convert
        # it into a real JSON is invoke: json.dumps(self.__space) and voila!

    def assign_car(self, car: Car, token) -> bool:
        """
        This method will allocate a spot to a car. Needless to say we need to acquire the semaphore first before we
        allocate the car
        """
        self.__slots.acquire()
        self.__space[token] = car # and we will then use the token that's provided to mark our car. In Java, this is
        # equivalent to saying map.put(token, car)
        return True

    def release_car(self, token: str) -> Car | None:
        """
        That's a funny looking syntax of the return type isn't it? ;) but all its trying to say is this method will either
        return a car or None. Now this, in spite of being specific what it is doing, feels a bit odd because in Java
        you can return a null even when the return type is an Object. Is it because Null is a type of Object? if yes why?
        if no, why? - interview question! :)
        Spoiler alert - ABSOLUTELY NOT! The Java language specification clearly says "null is a special type" and that
        it is impossible to declare anything of null type (4.1. The Kinds of Types and Values). Javascript does something
        funny. Fire up the browser console and type: typeof(null) and you get the answer 'object' :) :). This is the
        reminiscent bug of the earlier versions of javascript when it was developed by Netscape that unfortunately cannot
        be fixed without breaking the code. Bottomline: in my view, Python does the correct thing here saying this
        method can return a Car or None if it is not able to locate the car to be removed from the slot.
        """

        car_dict = {t:c for (t, c) in self.__space.items() if t == token} # this is running a loop with the variable (t,c)
        # in __space.items() and filtering the one where the value of t == token and then returning t:c. This is similar
        # to the filter operation that we do using streams in Java, but its much sweeter.
        # Its called dictionary comprehension

        if car_dict[token]:
            car_dict[token].assign_token(None) # if we locate the car, we nullify the token
            self.__slots.release() # we release the hold on the semaphore
            return car_dict[token] # and we return the car
        else:
            return None # otherwise we return None

    def has_empty_slots(self) -> bool: # utility method.
        return len(self.__space) < AVAILABLE_SLOTS

    def is_slot_filled(self) -> bool: # utility method.
        return len(self.__space) > 0

    def available_slots(self) -> int: # utility method.
        return len(self.__space)

    def empty_slots(self) -> int: # utility method.
        return AVAILABLE_SLOTS - self.available_slots()


class Vallet:
    """
    Let's define a vallet person who will do the job of actually parking and unparking the car. This person has access
    to the parking lot which is initialized in the constructor below.
    """
    def __init__(self, parking_lot) -> None:
        self.parking_lot = parking_lot

    def park(self, car: Car) -> tuple[UUID, str] | tuple[None, str]:
        """
        Dont get intimidated by the return type here. It's the same thing again. You either return a tuple of uuid and a
        string or your return a tuple of None and string. A tuple is an immutable data type which stores multiple values
        So here you have an example in which multiple return values are packed into a tuple and returned from a function
        Java lacks this feature out of the box. Yes you can import libraries and do the same but python has it inbuilt!
        """
        if self.parking_lot.has_empty_slots(): # so we check if the parking lot has empty slots. IF there are...
            token = uuid.uuid4() # we generate a unique identifier using the standard library
            car.assign_token(token) # and assign the token to the car for unique identification.
            self.parking_lot.assign_car(car, token) # finally, we assign the car to the parking lot.
            return token, car.owner # and return the token and the car owner's name for bookkeeping.
        else:
            return None, car.owner # else we return a None indicating the car couldn't be parked as the slots were not empty

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
