import threading
import time
import random

import requests
from lxml import html

BASE_URL = 'http://finance.yahoo.com/quote/'
HEADERS = {'User-Agent': "Mozilla/6.0 (X11; Ubuntu; Linux i586; rv:49.0) Gecko/20200202 Firefox/49.0"}


class YahooFinanceWorkerV1(threading.Thread):
    def __init__(self, symbol, **kwargs):
        super(YahooFinanceWorkerV1, self).__init__(**kwargs)
        self._symbol = symbol
        self._url = f'{BASE_URL}{symbol}?p={symbol}'
        self.start()


    def run(self):
        time.sleep(30 * random.random()) # introducing a delay so as to NOT spam Yahoo
        r = requests.get(self._url, headers=HEADERS)

        if r.status_code != requests.codes.ok:
            return

        page_contents = html.fromstring(r.content)
        price_element = page_contents.xpath(
            '//*[@id="nimbus-app"]/section/section/section/article/section[1]/div[2]/div[1]/section/div/section[1]/div[1]/div[1]/span')
        if price_element:
            print(f"price of {self._symbol} =  {price_element[0].text}")
        else:
            print(f"could not find price for {self._symbol}")

