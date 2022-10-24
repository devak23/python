import time


def countdown(n: int) -> None:
    while n > 0:
        print(f'T minus {n}')
        n -= 1
        time.sleep(1)
    result = 'We have Lift off!' if n == 0 else "Count down stopped!"
    print (result)


if __name__ == '__main__':
    print('Main thread started')
    from threading import Thread
    t = Thread(target=countdown, args=(10,))
    t.start()
    print('\rMain thread completed')
