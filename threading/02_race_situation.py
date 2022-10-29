# let's consider a program that reads a website and writes the content to a file
import io
import threading
from urllib.request import urlopen


class Crawler:

    def grab_content(self, urls: list, f: io.TextIOWrapper) -> None:
        while urls:
            url = urls.pop()
            print(f'doing {url} now...')
            f.writelines(str(urlopen(url).read()))
            f.write("=================================================")


def main() -> None:
    urls1 = ['http://www.google.com', 'http://www.facebook.com']
    urls2 = ['http://www.yahoo.com', 'http://www.youtube.com']

    f = open('output1.txt', 'w+')
    c = Crawler()
    t1 = threading.Thread(target=c.grab_content, args=(urls1, f))
    t1.start()

    t2 = threading.Thread(target=c.grab_content, args=(urls2, f))
    t2.start()


if __name__ == '__main__':
    main()
