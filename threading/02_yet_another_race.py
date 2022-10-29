# Race conditions, like any other failures are pesky things designed to torture you in professional life alluding you
# towards alcohol, smoking, drugs and the other vices. However, we don't have to go that far. Programming languages
# offer simple constructs like synchronization to prevent you from doing substance abuse. Ofcourse, I am preaching
# to the choir ... so let's dive into code and see how python does these things in action.

# For our simplistic toy example (and really, that's the limit of my technical super-strength here), we are going to
# have 2 different..no... 3 different emitters A.K.A producers for the techies! :( emitting 3 different quotes and
# 3 consumers writing them into a text file. Like a sadist, we will watch them all getting jumbled up and laugh
# out loud (like The Devil/Satan/Iblis/Yamraaj/Lucifer ... ooh! that's cool series on Netflix! Have you seen it?)
# And about that laughter, really?? Why does the evil have to laugh out loud? I don't get it. You designed it that way
# and it worked... so? what's the big story here? I mean programmers do this all the damn time! You don't see me
# laughing after this program working the way I wanted it work, do you? Such a cliché I tell you!

from collections import namedtuple
from queue import Queue
from threading import Thread
import time

# So we define a value holder class called as the HolyBook. You must be a pro by now to understand and use this snippet.
# For those who were dozing, it creates a class on the fly with two attributes - name and quote in it.
HolyBook = namedtuple('HolyBook', ['name', 'quote'])


class Preacher:
    """
    And we define a Preacher whose job is to read a quote from his book and preach the meaning to the masses. So we will
    have him/her have a name (like 'Padre', 'Maulvi' or 'Guru') and a "queue" of quotes with who can expand on the
    ideas of quotes. Finally, we also need a 'flag' which can instruct him/her if he can preach or not.
    """
    def __init__(self, name: str, book: HolyBook):
        self.__quotes = Queue()  # YES! this time we are using the actual queue instead of using my own creation :P
        self._name = name
        self._book = book
        self._can_preach = True

    def preach(self, masses: str):
        """
        This is the behavior where the preacher will "preach" (write) the quote it gets from the queue into a file called
        masses.txt
        """

        # BTW... this is how you do a try-catch in python... Quite easy and pretty much same as Java!
        try:
            # So we are saying while the preacher is allowed to preach and if the quotes are available,
            while self._can_preach and self.__quotes.qsize():
                # we will open a file in an "append" mode and ...
                with open(file=masses, mode='a') as f:
                    # we keep on writing into the file.
                    f.write(self.__quotes.get() + "\r\n")
        except IOError:
            print("Couldn't preach!")
        # After the preacher is done we delcare so. No brilliance here if you were expecting one :)
        print(f'{self._name}: Done preaching!')

    def stop_preaching(self):
        """
        And this method will signal the preacher that he/she may stop preaching now.
        """
        self._can_preach = False

    def prepare_for_sermon(self) -> None:
        # since I absolutely lack creativity, I am gonna just populate the same quote over and over till you guys fall asleep.
        while self.__quotes.qsize() < 100:
            self.__quotes.put(self._book.quote)
        print(f"Quotes populated from {self._book.name}")


def main() -> None:
    # Let's create an instance of the Holy books.
    Bible = HolyBook('Bible',
                     '[Corinthians 11:14] - And no wonder, for Satan himself masquerades as an angel of light.')
    Quran = HolyBook('Quran',
                     '[Quran 2:208] - O you who believe, you shall embrace total submission; do not follow the steps of Satan, for he is your most ardent enemy.')
    Gita = HolyBook('Gita',
                    '[Gita 16:4] - Arrogance, pride, anger, conceit, harshness and ignorance-these qualities belong to those of demonic nature, O Partha.')
    print("Created the holy books.")

    # We will give each preacher the books containing the quotes
    father = Preacher('Father', Bible)
    guru = Preacher('Guru', Gita)
    maulvi = Preacher('Maulvi', Quran)
    print("Preachers created.")

    # and we will ask the preachers to prepare for the sermon i.e.populate queues from the respective holy books
    maulvi.prepare_for_sermon()
    guru.prepare_for_sermon()
    father.prepare_for_sermon()

    # These 3 distinguished folks are now going to "preach the masses" (the audience is masses.txt), so let's have them
    # going in a thread.
    tmaulvi = Thread(target=maulvi.preach, args=("masses.txt",))
    tguru = Thread(target=guru.preach, args=("masses.txt",))
    tfather = Thread(target=father.preach, args=("masses.txt",))
    print("Created threads for the preachers...")

    # Notice how we have the same audience for all the 3 religious speakers and that's where the race will be seen
    tmaulvi.start()
    tguru.start()
    tfather.start()
    print("Preachers have started preaching...")

    # We will wait for 5 seconds and then ask each of them to stop preaching
    print("Waiting for 5 seconds for the preachers to preach the masses...")
    time.sleep(5)

    # This ofcourse breaks the loop by setting the 'flag' to false.
    guru.stop_preaching()
    father.stop_preaching()
    maulvi.stop_preaching()
    print("Preachers have been asked to stop preaching.")

    print("Waiting for threads to complete...")
    tfather.join()
    tguru.join()
    tmaulvi.join()

    # and we are done! Now take a look inside the masses.txt and you should expect all the quotes jumbled up.
    print('Done!')


if __name__ == '__main__':
    main()
