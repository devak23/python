import multiprocessing
import requests

websites = [
    'https://www.rbi.org.in/',
    'https://www.india.gov.in/',
    'https://www.oreilly.com/',
    'https://www.apple.com/',
    'https://www.google.com/',
    'https://www.microsoft.com',
]


def visit_websites(urls: list):
    for url in urls:
        r = requests.get(url)
        print(f'{url} returned {r.status_code} after {r.elapsed} seconds')


def visit_website(url: str):
    r = requests.get(url)
    print(f'{url} returned {r.status_code} after {r.elapsed} seconds')


if __name__ == "__main__":
    # p1 = multiprocessing.Process(target=visit_websites, args=(websites,))
    # p1.start()
    # p1.join()

    procs = [multiprocessing.Process(target=visit_website, args=(url,)) for url in websites]
    for proc in procs:
        proc.start()

    for proc in procs:
        proc.join()
