from concurrent.futures import ThreadPoolExecutor
import requests

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
    with ThreadPoolExecutor(max_workers=2) as executor:
        for w in websites:
            executor.submit(visit_website, w)

    print('Main thread completed')