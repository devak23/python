# In this example we explore another form of synchronization called Condition variables. Did you explore that in Java? :)
# I am guessing not! ... cause lets face it, no such need arose. But "condition variables exist all around us" like the
# Matrix! :) Please tell me you watched that movie and it was phenomenal. I had to watch it twice just to understand
# what was the heck was going on.
#
# SIDE NOTE: I read it in a review that the movie was inspired by the concept of 'Maya' in Hindu philosophy.
# Maya who ... you ask? No no, this one is like the colloquial hindi phrase "Moh-Maya" :) which BTW is a very diluted
# and highly abused form of the actual concept. The concept of Maya was doctored by Shri Shankaracharya a landmark in
# the advancement of the "Advaita Vedanta philosophy" whose gist is "You and HIM/HER are one and the same".
# It goes quite deep should you have an inclination to learn it.
#
# But we are dealing with the materialistic world here so coming back... imagine two friends - a Caller and Callee
# calling each other and talking about office problems...what else is new? :( The caller calls and awaits till the
# connection is established, rants for sometime about how bad his/her day went and hangs up after the conversation
# is over. Sounds BAU... no?
#
# We will simulate that in following program using condition variable. Note: the word "condition" is suggestive of the
# fact that synchronization will happen based on "satisfaction of a condition". Let' see how...

import time
from threading import Condition, Thread


class Friend:
    def __init__(self, name, phone_call: Condition) -> None:
        """
        # We define a 'Friend' (Caller) class who has a name and a phone.
        """
        self.name = name
        self.__phone = phone_call

    def call(self, callee: str) -> None:
        """
        The Friend can "call" another friend (callee). So think of this method from the caller's point of view here.
        Since this method doesn't do much, a None is returned
        """
        self.__phone.acquire()  # we dial the friend's number.
        # In technical terms we acquire a lock on the Condition variable.
        print(f'{self.name} calling {callee}')

        self.__phone.wait()  # and we hold while it rings on the other end of the line.
        # In short, the thread will be blocked here waiting for a 'notification' from the other end

        print(f'{self.name} is now talking to {callee}')
        time.sleep(3)  # only to simulate a feel of conversation.
        print(f'Conversation is over. {self.name} disconnected the call')

        self.__phone.release()  # Once we are done, we disconnect the call.
        # In technical terms, we will release the hold on the condition variable.

    def receive(self, caller: str) -> None:
        """
        Similarly, "this other Friend" can receive a phone call from the Caller. So think of this method from the
        callee's point of view. Again since this method doesn't do much, a None is returned
        """
        print(f'{self.name} receiving the call')
        time.sleep(1)  # only to simulate a delay of getting the call.

        self.__phone.acquire()  # Callee grabs the phone aka: secures the lock on the condition variable.
        print(f'{self.name} picks up the receiver and greets')
        self.__phone.notify()  # THIS, RIGHT HERE... IS VERY IMPORTANT! the notify() as mentioned in the introduction
        # signals that the condition is satisfied between the two threads. The callee is now in sync with the caller
        # and two can communicate.

        print(f'{self.name} is now talking to {caller}')
        time.sleep(3) # only to simulate a conversation
        self.__phone.release()  # again, when call is done, we release the hold on the condition variable which allows
        # the thread to resume its job.


def main() -> None:
    # define a condition variable.
    phone = Condition()

    # and we create 2 friends passing in the condition variable (phone).
    friend1 = Friend('Kavita Y', phone)
    friend2 = Friend('Kavita K', phone)

    tfriend1 = Thread(target=friend1.call, args=(friend2.name,))
    # Friend1 initiates the call and hence we pass the 'call' method into the "target"

    tfriend2 = Thread(target=friend2.receive, args=(friend1.name,))
    # Friend2 receives the call and hence we pass the 'receive' method into the "target"

    tfriend1.start()
    time.sleep(1)  # only to simulate a connection delay.
    tfriend2.start()

    tfriend1.join()
    tfriend2.join()

    print('Phone call successfully ended.')


if __name__ == '__main__':
    main()
