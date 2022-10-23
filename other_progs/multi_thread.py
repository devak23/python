import requests
import threading

websites = [
    'https://www.rbi.org.in/',
    'https://www.india.gov.in/',
    'https://www.oreilly.com/',
    'https://www.apple.com/',
    'https://www.google.com/',
    'https://www.microsoft.com',
]


def visit_website(url):
    r = requests.get(url)
    print(f'{url} returned {r.status_code} after {r.elapsed} seconds')


if __name__ == '__main__':
    print('Main thread started')
    for w in websites:
        t = threading.Thread(target=visit_website, args=[w])
        t.start()
    print('Main thread completed')
