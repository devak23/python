import random
import threading
import time
from threading import Semaphore


class Employee(threading.Thread):
    def __init__(self, name: str, zoom_number: threading.Semaphore) -> None:
        super().__init__()
        self.zoom_number = zoom_number
        self.__name = name
        self.__disconnect = False

    def start(self) -> None:
        delay = random.randint(1, 5)
        time.sleep(delay)
        self.zoom_number.acquire()
        print(f'{self.__name} joined the call... [delay = {delay} seconds]')

    def disconnect(self) -> None:
        print(f'{self.__name} has disconnected')
        time.sleep(1)
        self.zoom_number.release()


class Scrum(threading.Thread):
    def __init__(self, name, zoom_number: threading.Semaphore):
        super().__init__()
        self._name = name
        self.zoom_number = zoom_number
        self.__disconnect = False

    def start(self) -> None:
        self.zoom_number.acquire()
        print(f'{self._name} has started...')

    def end(self) -> None:
        self.zoom_number.release()
        print(f'{self._name} ended.')


def main() -> None:
    # this will be our synchronizing mechanism.
    zoom_number = Semaphore(7)

    # let's create the participants of the call.
    suhas = Employee('Suhas', zoom_number)
    kavitak = Employee('Kavita K', zoom_number)
    junaid = Employee('Junaid', zoom_number)
    saif = Employee('Saif', zoom_number)
    nitin = Employee('Nitin', zoom_number)
    kavitay = Employee('Kavita Y', zoom_number)

    # let's create the instance of a scrum call itself which needs to begin for people to start connecting.
    scrum = Scrum('APAC scrum call', zoom_number)

    # and let's start the scrum call...
    scrum.start()

    #  We will now create a thread of each employee trying to join the call
    suhas.start()
    kavitak.start()
    junaid.start()
    saif.start()
    nitin.start()
    kavitay.start()

    print("People are now discussing in the scrum call")
    time.sleep(3)  # simulating the discussion
    scrum.end()  # ending the call

    # The threads will release the hold on the semaphore as well. That is tantamount to disconnecting from the call.
    suhas.disconnect()
    kavitak.disconnect()
    junaid.disconnect()
    saif.disconnect()
    nitin.disconnect()
    kavitay.disconnect()

    print("Call is over.")


if __name__ == '__main__':
    main()
