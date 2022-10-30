# In this example we explore another form of synchronization called Condition variables. Did you explore that in Java? :)
# I am guessing not! ... cause lets face it, no such need arose. But "condition variables exist all around us" like the
# Matrix! :) Please tell me you watched that movie and it was phenomenal. I had to watch it twice just to understand
# what was the heck was going on. I read it in a review that the movie was inspired by the concept of 'Maya' in
# Hindu philosophy. Maya who ... you ask? No, this one is like the colloquial hindi phrase "Moh-Maya" :) which is a very
# diluted and highly abused form of the actual concept. The concept of Maya was doctored by Shri Shankaracharya a
# pioneer in the advancement of the "Advaita Vedanta philosophy" whose gist was you and HIM/HER are one and the same
# thing. It goes quite deep if one has an inclination to learn it.
#
# But we are dealing with the materialistic world here so coming back... imagine two friends calling each other. Caller
# calls and awaits till the connection is established and hangs up after the conversation is over. We will simulate that
# in following program. The word Condition itself states that the synchronization will happen based on satisfaction of
# a condition. Let' see how...

import time
from threading import Condition, Thread


# We define a 'Friend' class who has a name and a phone.
class Friend:
    def __init__(self, name, phone_call: Condition):
        self.name = name
        self.__phone = phone_call

    def call(self, callee: str):
        """
        The Friend can "call" another friend (callee). So think from the caller's point of view here.
        """
        self.__phone.acquire()  # we dial the friend's number (in technical terms we acquire a lock on the Condition variable)
        print(f'{self.name} calling {callee}')
        self.__phone.wait()  # and we hold while it rings on the other end. In short, the thread will be blocked here waiting for a 'notification' from the other end
        print(f'{self.name} is now talking to {callee}')
        time.sleep(1)  # only to simulate a feel of conversation.
        print(f'Conversation is over. {self.name} disconnected the call')
        self.__phone.release()  # ofcourse once we are done, we disconnect the call. In tech terms, we will release the hold on the condition variable.

    def receive(self, caller: str):
        """
        Similarly, we can receive a phone call from our friend (caller). So think from the callee's point of view here.
        """
        print(f'{self.name} receiving the call')
        time.sleep(1)  # only to simulate a delay of getting the call.
        self.__phone.acquire()  # Callee grabs the phone aka: secures the lock on the condition variable.
        print(f'{self.name} picks up the receiver and greets')
        self.__phone.notify()  # THIS, RIGHT HERE... IS VERY IMPORTANT! the notify() signals that the callee is now in sync with the caller thread.
        print(f'{self.name} is now talking to {caller}')
        self.__phone.release()  # again, when call is done, we release the hold on the condition variable.


def main() -> None:
    phone = Condition()
    friend1 = Friend('Sana', phone)
    friend2 = Friend('Kavita', phone)

    tfriend1 = Thread(target=friend1.call, args=(friend2.name,))
    tfriend2 = Thread(target=friend2.receive, args=(friend1.name,))

    tfriend1.start()
    time.sleep(1)  # only to simulate a connection delay.
    tfriend2.start()

    tfriend1.join()
    tfriend2.join()

    print('Phone call successfully ended.')


if __name__ == '__main__':
    main()
