# lets consider a program that reads a website and writes the content to a file
import io
import threading
import urllib.error
from urllib.request import urlopen


class Crawler:

    def __init__(self, lock: threading.Lock):
        self.__lock = lock

    def grab_content(self, urls: list, f: io.TextIOWrapper) -> None:
        while urls:
            self.__lock.acquire()
            print(f'Lock acquired')
            try:
                url = urls.pop()
                print(f'doing {url} now...')
                f.writelines(str(urlopen(url).read()))
                f.write("=================================================")
            except (urllib.error.URLError, urllib.error.HTTPError, IOError):
                print(f'lookup failed')
            self.__lock.release()
            print(f'Lock released')


def main() -> None:
    urls1 = ['http://www.google.com', 'http://www.facebook.com']
    urls2 = ['http://www.yahoo.com', 'http://www.youtube.com']

    f = open('output2.txt', 'w+')
    lock = threading.Lock()
    c = Crawler(lock)
    t1 = threading.Thread(target=c.grab_content, args=(urls1, f))
    t1.start()

    t2 = threading.Thread(target=c.grab_content, args=(urls2, f))
    t2.start()


if __name__ == '__main__':
    main()
