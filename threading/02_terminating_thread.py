import time


class Counter:
    def __init__(self) -> None:
        self._running = True

    def stop(self) -> None:
        self._running = False

    def countdown(self, n) -> None:
        while self._running and n > 0:
            print(f'T minus {n}')
            n -= 1
            time.sleep(1)
        result = 'Lift off!' if n == 0 else 'Count down aborted!'
        print(result)


if __name__ == '__main__':
    print('Main Thread started')
    counter = Counter()
    from threading import Thread

    t = Thread(target=counter.countdown, args=(10,))
    t.start()

    time.sleep(5)
    counter.stop()
    t.join()
    time.sleep(1)
    print('Main Thread completed')
