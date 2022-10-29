# Race conditions, like any other failures are pesky things designed to torture you in professional life alluding you
# towards alcohol, smoking, drugs and the other vices. However, we don't have to go that far. Programming languages
# offer simple constructs like synchronization so as prevent you from doing substance abuse. Ofcourse, I am preaching
# to the choir here... so let's dive into code and see how python does these things in action.

# For our simplistic toy example (and really, that's the limit of my technical super-strength here), we are going to
# have 2 different..no... 3 different emitters A.K.A producers for the techies! :( emitting 3 different sentences and
# 3 threads writing them into a same text file and like a sadist, we will watch them all getting jumbled up and laugh
# out loud (like The Devil/Satan/Iblis/Yamraaj/Lucifer ... ooh! that's cool series on Netflix! Have you seen it?)

from collections import namedtuple
from queue import Queue
from threading import Thread, Lock
import time

HolyBook = namedtuple('HolyBook', ['name', 'quote'])


class Preacher:
    def __init__(self, name: str, quotes: Queue, lock: Lock):
        self._quotes = quotes
        self._name = name
        self.__can_preach = True
        self.__lock = lock

    def preach(self, masses: str):
        try:
            self.__lock.acquire()
            while self.__can_preach and self._quotes.qsize():
                with open(file=masses, mode='a') as f:
                    f.write(self._quotes.get() + "\r\n")
            self.__lock.release()
        except IOError:
            print("No masses found! Cannot preach")
        print(f'{self._name}: Done preaching!')

    def stop_preaching(self):
        self.__can_preach = False


def populate_queue(queue: Queue, book: HolyBook) -> None:
    # since we don't have a large repo of quotes, we are going to just populate the same quote in the queue
    while queue.qsize() < 50:
        queue.put(book.quote)
    print(f"populated queue from {book.name}")


if __name__ == '__main__':
    # Let's create an instance of Holy books.
    Bible = HolyBook('Bible',
                     '[Corinthians 11:14] - And no wonder, for Satan himself masquerades as an angel of light.')
    Quran = HolyBook('Quran',
                     '[Quran 2:208] - O you who believe, you shall embrace total submission; do not follow the steps of Satan, for he is your most ardent enemy.')
    Gita = HolyBook('Gita',
                    '[Gita 16:4] - Arrogance, pride, anger, conceit, harshness and ignorance-these qualities belong to those of demonic nature, O Partha.')
    print("Created the holy books.")

    # and let's create 3 different queues which will receive quotes from these holy books. YES! this time we are using
    # the actual queue instead of a list.
    quotes_from_gita = Queue()
    quotes_from_bible = Queue()
    quotes_from_quran = Queue()
    print("Created the queues.")

    # and populate these queues from the respective holy books
    tq = Thread(target=populate_queue, args=(quotes_from_quran, Quran))
    tg = Thread(target=populate_queue, args=(quotes_from_gita, Gita))
    tb = Thread(target=populate_queue, args=(quotes_from_bible, Bible))
    print("...started populating the queues from the holy books.")

    tq.start()
    tb.start()
    tg.start()

    # Now we have the producers going, lets create consumers
    lock = Lock()
    padre = Preacher('Father', quotes_from_bible, lock)
    guru = Preacher('Guru', quotes_from_gita, lock)
    maulvi = Preacher('Maulvi', quotes_from_quran, lock)
    print("Preachers created.")

    # These 3 distinguished folks are now going to preach the masses, so let's have them going
    tmaulvi = Thread(target=maulvi.preach, args=("masses.txt",))
    tguru = Thread(target=guru.preach, args=("masses.txt",))
    tpadre = Thread(target=padre.preach, args=("masses.txt",))
    print("Created threads for the preachers...")

    # Notice how we have the same audience for all the 3 religious speaker and that's where the race will be seen
    tmaulvi.start()
    tguru.start()
    tpadre.start()
    print("Preachers have started preaching...")

    # We now wait for 10 seconds and then ask each of them to stop preaching
    print("Waiting for 10 seconds for the preachers to preach the masses...")
    time.sleep(10)

    guru.stop_preaching()
    padre.stop_preaching()
    maulvi.stop_preaching()
    print("Preachers have been asked to stop preaching.")

    print("Waiting for threads to complete...")
    tpadre.join()
    tguru.join()
    tmaulvi.join()

    # and we are done!
    print('Done!')
