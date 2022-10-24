import time
from threading import Thread, Event


class Counter:
    def __init__(self, name):
        self._name = name

    def countdown(self, n: int, event_start: Event) -> None:
        if event_start.is_set():
            print(f'Count down for {self._name} has started...')
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
    c1 = Counter('Apollo 13')
    c2 = Counter('Falcon 12')
    countdown_event = Event()
    t1 = Thread(target=c1.countdown, args=(10, countdown_event))
    t1.start()

    time.sleep(1)
    countdown_event.set()
    t2 = Thread(target=c2.countdown, args=(10, countdown_event))
    t2.start()
    t2.join()
    t1.join()
    time.sleep(1)
    print('Main thread completed')
