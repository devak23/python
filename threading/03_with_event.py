import time
from threading import Thread, Event


class Counter:
    """
    Checking for a thread termination can be tricky to co-ordinate. A fine-grained control can be employed by creating
    something called an Event exposed by the thread library. Events are best for 'one-time-events'. It is possible
    to use the api to 'clear()' the event and reusing it again, but why perform such jugglery if you can do better?
    """
    def __init__(self, name):
        # just an identifier for the thread.
        self._name = name

    def countdown(self, n: int, event_start: Event) -> None:
        """
        So now the method takes in not only an integer to count down to, but also an 'Event' which will tell us
        if the event has started or not.
        """
        if event_start.is_set():
            while n > 0:
                print(f'{self._name}: T minus {n}')
                n -= 1
                time.sleep(1)
            result = f"{self._name}: We have Lift off!" if n == 0 else f"Count down Aborted for {self._name}!"
            print(result)
        else:
            print(f'Launch event has not started for {self._name}')


if __name__ == '__main__':
    print('Main thread started')

    # Create two counters for our Rockets
    c1 = Counter('Apollo 13')
    c2 = Counter('Falcon 12')
    countdown_event = Event()
    t1 = Thread(target=c1.countdown, args=(10, countdown_event))
    t1.start()

    time.sleep(1) # just a second pause before we start the event.
    countdown_event.set()
    print('Launch event is initiated...')
    t2 = Thread(target=c2.countdown, args=(10, countdown_event))
    t2.start()
    t2.join()
    t1.join()
    time.sleep(1) # another pause to signal the termination of main thread.
    print('Main thread completed')
