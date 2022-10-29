# Fortunately, our masses did their homework pretty well and therefore even if the output is jumbled up, they can figure
# out to themselves what the preacher was talking about. But not all audiences can decipher a mixed output.

# Yawn,Yawn "I could see this from miles away. It doesn't need a Sherlock Holmes brain to figure out what will happen
# when all the threads write into the same file" - You condescend me :( But you have learnt Java, so you know the trick.
#
# Ofcourse you are right! But now how do we solve it? ... "Elementary, my dear Watson!" -  LOCKS!!!
# I know it's not as flashy as it sounds, but remember, we are just speaking a different language here (no pun intended)
# The concept will still remain the same only the syntax changes. So here we go again...

from collections import namedtuple
from queue import Queue
from threading import Thread, Lock
import time

HolyBook = namedtuple('HolyBook', ['name', 'quote'])


class Preacher:
    def __init__(self, name: str, book: HolyBook, lock: Lock):
        """
        The curtain rises! Now the Preacher is given a "Lock" object from the 'threading package'. This lock object
        will allow him/her to preach only if he/she can acquire it in the first place.
        """
        self.__quotes = Queue()  # Did you notice how the other variables are protected and this one being private?
        self._name = name
        self._book = book
        self._can_preach = True
        self._lock = lock

    def preach(self, masses: str):
        try:
            # The preacher will first try to acquire the lock. If that is successful, preaching follows...
            self._lock.acquire()
            while self._can_preach and self.__quotes.qsize():
                with open(file=masses, mode='a') as f:
                    f.write(self.__quotes.get() + "\r\n")
            # After all is done, the lock is released and the other preacher can get it.
            self._lock.release()
        except IOError:
            print("No masses found! Cannot preach")
        print(f'{self._name}: Done preaching!')

    def stop_preaching(self):
        self._can_preach = False

    def prepare_for_sermon(self) -> None:
        while self.__quotes.qsize() < 100:
            self.__quotes.put(self._book.quote)
        print(f"Quotes populated from {self._book.name}")


def populate_queue(queue: Queue, book: HolyBook) -> None:
    while queue.qsize() < 50:
        queue.put(book.quote)
    print(f"populated queue from {book.name}")


def main() -> None:
    # as before, we create the Holy Books
    Bible = HolyBook('Bible',
                     '[Corinthians 11:14] - And no wonder, for Satan himself masquerades as an angel of light.')
    Quran = HolyBook('Quran',
                     '[Quran 2:208] - O you who believe, you shall embrace total submission; do not follow the steps '
                     'of Satan, for he is your most ardent enemy.')
    Gita = HolyBook('Gita',
                    '[Gita 16:4] - Arrogance, pride, anger, conceit, harshness and ignorance-these qualities belong '
                    'to those of demonic nature, O Partha.')
    print("Created the holy books.")

    # and we create an instance of a Lock object. Very important!!
    lock = Lock()

    # We will give each preacher the book containing the quotes and the lock which they can hold. The first one to hit
    # the buzzer gets to deliver his/her sermon! So they will have to play "fastest finger first"
    father = Preacher('Father', Bible, lock)
    guru = Preacher('Guru', Gita, lock)
    maulvi = Preacher('Maulvi', Quran, lock)
    print("Preachers created.")

    # and we will ask the preachers to prepare for the sermon i.e.populate queues from the respective holy books
    maulvi.prepare_for_sermon()
    guru.prepare_for_sermon()
    father.prepare_for_sermon()

    # Again, we create 3 threads to get the preaching going...The audience is common for all the 3 preachers: masses.txt
    tmaulvi = Thread(target=maulvi.preach, args=("masses.txt",))
    tguru = Thread(target=guru.preach, args=("masses.txt",))
    tfather = Thread(target=father.preach, args=("masses.txt",))
    print("Created threads for the preachers...")

    tmaulvi.start()
    tguru.start()
    tfather.start()
    print("Preachers have started preaching...")

    # We now wait for 5 seconds and then ask each of them to stop preaching
    print("Waiting for 5 seconds for the preachers to preach the masses...")
    time.sleep(5)

    guru.stop_preaching()
    father.stop_preaching()
    maulvi.stop_preaching()
    print("Preachers have been asked to stop preaching.")

    print("Waiting for threads to complete...")
    tfather.join()
    tguru.join()
    tmaulvi.join()

    # now take a look, and you should see all the preachers have gotten to all their quotes in their time slice. The
    # output file is much ordered now.
    print('Done!')


if __name__ == '__main__':
    main()

# so the audience now listened to each preacher and could understand what they said for that duration of time before
# moving on to the next one. THAT! my dear friend is how we can do synchronization in python. There are more
# synchronization elements and we will go over it one by one, but that's all for today. See you next Friday!