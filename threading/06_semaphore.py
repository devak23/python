# So using a condition variable allows us to synchronize between two threads. But what if you had to synchronize
# across multiple threads? Like how would you allow a "controlled access" to a certain number of threads? Any
# guesses? Well a semaphore comes to the rescue. Apparently, semaphore was invented by a Dutch computer scientist -
# Edseger Dijkstra :( Not only his inventions are pain, but so is his name! I believe keeping English as the world's
# communication language for a foreseeable future all the languages of the world including mine really ought to
# "normalize" the names that are easily pronounceable. I mean c'mmon... Edseger Dijkstra? As an Indian myself,
# I pronounced his name as the syllables were introduced to me in kindergarten - "Ed-say-ger dee-juk-stra". I know I
# inserted the 'u' there, but I couldn't really pronounce jk together without making an "u" sound. I know ... lame!
# :( Anyways, my way of pronunciation of that name doesn't have a nice ring to it. So I googled :| It turns out,
# the name is pronounced "ets-kar daa-eek-stra" with a very rounded D and T sounds (not sharp as in "dot" in english)
# :| Now, why does there have to be a j in his first name? :| Well, only the "dutchman" knows, but the point is Mr.
# Dijkstra being genius and all managed to get us into trouble by investing his time into algorithms. This is a
# classic case of someone enjoying the cake and someone else footing the bill :( ... Anyways, Dijkstra's famous
# "Shortest Path Algorithm" is well known in the field of Computer Science. When I say "well known", I mean it is
# known to a lot many people, EXCEPT ME! :| Now, depending on your career aspirations or your desire to socialize
# with the "tech gurus" within the company, you might choose to know/study it. For the rest of lesser mortals like
# me, as long as the "GPS lady" correctly guides you from Sodawala Lane (Borivali) to Zhaveri Baazar (Kalbadevi),
# you are sorted ;)
#
# I have digressed... as I usually do :|. So, coming back, semaphore is a fancy word for "flag". This flag is
# basically a signal used for communicating with another thread. Ever seen railway folks wave a physical flag to an
# incoming/ outgoing trains? THAT! my friend is a real life semaphore. In the software universe, a semaphore will
# allow communication between specific # of threads and enable concurrency. You could achieve the same goal with
# locks and a counter, but why re-invent the wheel when a Semaphore is handy? Typically, you initialize a Semaphore
# by a count and then keep on "acquiring it". After a certain point the acquire call will block all the future
# invocations and the method/ behavior /critical section is protected thereby providing concurrency/synchronization
# as desired.
#
# Let's try to understand this by simulating a "parking lot problem" that we experience in everyday life. A very
# standard interview question ;). So we know there are specific # of slots in a parking lot. Any additional cars
# that come in will have to wait till somebody clears off their slot. That's what we will attempt to build using
# semaphores. Let's get into it.
import time
import uuid
from concurrent.futures import ThreadPoolExecutor
from threading import Semaphore
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

    def __repr__(self) -> str:  # toString() method
        return f"{self.owner}'s car"


class ParkingLot:
    """
    A parking lot will define slots which will be our Semaphore that will control how many cars can come in. It also
    has a physical space initialized by a dictionary object (Map in Java)
    """

    def __init__(self) -> None:
        self.__slots: Semaphore = Semaphore(AVAILABLE_SLOTS)
        self.__space: dict = {}  # the nice thing is the dict looks like a JSON in python :) All you got to do is
        # invoke: json.dumps(self.__space) and voilà it gets converted into a JSON.

    def assign_car(self, car: Car) -> str:
        """
        This method will allocate a spot to a car. Needless to say we need to acquire the semaphore first before we
        allocate the car
        """

        self.__slots.acquire()
        token = str(uuid.uuid4())  # we generate a unique identifier using the standard library
        self.__space[token] = car  # and we will then use the token that's provided to mark our car. In Java, this is
        # equivalent to saying map.put(token, car)
        return token

    def release_car(self, token: str) -> Car | None:
        """
        That's a funny looking syntax of the return type isn't it? ;) but all its trying to say is this method will
        either return a car or None. Now this, in spite of being specific what it is doing, feels a bit odd because
        in Java you can return a null even when the return type is an Object. Is it because Null is a type of Object?
        if yes why? if no, why? - interview question! :) Spoiler alert - ABSOLUTELY NOT! The Java language
        specification clearly says "null is a special type" and that it is impossible to declare anything of null
        type (4.1. The Kinds of Types and Values). Javascript does something funny. Fire up the browser console and
        type: typeof(null) and you get the answer 'object' :) :). I don't know if this is intentional or a bug from
        the earlier versions of javascript when it was developed by Netscape. Long story short,  in my view,
        Python does the correct thing here saying this method can return a Car or None if it is not able to locate
        the car to be removed from the slot.
        """

        car_dict = {t: c for (t, c) in self.__space.items() if t == token}  # this is running a loop with the variable
        # (t,c) in __space.items() and filtering the one where the value of t == token and then returning t:c. This is
        # similar to the filter operation that we do perform with streams in Java, but much sweeter. It's called
        # dictionary comprehension.

        if car_dict[token]:
            car_dict[token].assign_token(None)  # if we locate the car, we nullify the token
            self.__slots.release()  # we release the hold on the semaphore
            return car_dict[token]  # and we return the car
        else:
            return None  # otherwise we return None

    def has_empty_slots(self) -> bool:  # utility method.
        return len(self.__space) < AVAILABLE_SLOTS

    def is_slot_filled(self) -> bool:  # utility method.
        return len(self.__space) > 0

    def available_slots(self) -> int:  # utility method.
        return len(self.__space)

    def empty_slots(self) -> int:  # utility method.
        return AVAILABLE_SLOTS - self.available_slots()


class Vallet:
    """
    Let's define a vallet person who will do the job of actually parking and unparking the car. This person has access
    to the parking lot which is initialized in the constructor below.
    """

    def __init__(self, parking_lot) -> None:
        self.parking_lot = parking_lot

    def park(self, car: Car) -> tuple[str, str] | tuple[None, str]:
        """
        Don't get intimidated by the return type here. It's the same thing again. You either return a tuple of str
        and a string or your return a tuple of None and string. A tuple is an immutable data type which stores
        multiple values So here you have an example in which multiple return values are packed into a tuple and
        returned from a function Java lacks this feature out of the box. Yes you can import libraries and do the same
        but python has it inbuilt!
        """
        if self.parking_lot.has_empty_slots():  # so we check if the parking lot has empty slots. IF there are...
            token = self.parking_lot.assign_car(car)  # we assign the car to the parking lot and get a token in return
            car.assign_token(token)  # we then assign the token to the car for unique identification.
            return token, car.owner  # and return the token and the car owner's name for bookkeeping.
        else:
            return None, car.owner  # else we return a None indicating the car couldn't be parked as the slots were
            # not empty

    def unpark(self, token: str) -> Car | None:
        if not token:  # ofcourse we return nothing if there is no token
            return None

        if self.parking_lot.is_slot_filled():  # if the lot is empty, what are we going to unpark?
            return self.parking_lot.release_car(token)  # and we unpark the car using the token
        else:
            raise RuntimeError('No car is present in the slot')  # or raise an error if no car with the given token is
            # found


# Finally the main method
def main() -> None:
    # let's create the parking lot
    parking_lot = ParkingLot()

    # the cars from the reporting team
    cars = [Car('Suhas'), Car('KavitaK'), Car('KavitaY'), Car('Junaid'), Car('Saif'), Car('Avinash'),
            Car('Nimisha'), Car('Tejas'), Car('Guru'), Car('Sana'), Car('Chinmay'), Car('Mohita'), Car('Purva'),
            Car('Sahana'), Car('Laxmi'), Car('Ashwani')]

    # Let's create the valet who has access to the parking lot
    valet = Vallet(parking_lot)

    # and yes! a ThreadPoolExecutor object which we can use instead of creating bare threads. You know this in Java
    # as the ExecutorService :) Here we use the "with" clause so that things like automatic closing of the
    # threads, file closing if you are doing io operation or doing exception handling etc. is taken by the runtime
    # itself rather than managing it ourselves. The "with construct" is very clean and improves code readability

    with ThreadPoolExecutor(max_workers=5) as tp: # so we create an instance of threadpool of 5 threads
        result = tp.map(valet.park, cars) # and we pass all the cars to it. The result is a list of futures objects

    for r in result: # let's iterate and print it
        print(r)


if __name__ == '__main__':
    main()
