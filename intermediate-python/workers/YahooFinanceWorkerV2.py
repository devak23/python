import threading
import time
import random

import requests
from lxml import html

BASE_URL = 'http://finance.yahoo.com/quote/'
HEADERS = {'User-Agent': "Mozilla/6.0 (X11; Ubuntu; Linux i586; rv:49.0) Gecko/20200202 Firefox/49.0"}

class YahooFinancePriceScheduler(threading.Thread):
    def __init__(self, input_queue, **kwargs):
        super(YahooFinancePriceScheduler, self).__init__(**kwargs)
        self._input_queue = input_queue
        self.start()

    def run(self):
        while True:
            val = self._input_queue.get() # blocking call
            if val == 'Done':
                break

            yahoo_finance_price_worker = YahooFinanceWorkerV2(symbol=val)
            price = yahoo_finance_price_worker.get_price()
            print(price)
            # time.sleep(random.random())



class YahooFinanceWorkerV2():
    def __init__(self, symbol, **kwargs):
        super(YahooFinanceWorkerV2, self).__init__(**kwargs)
        self._symbol = symbol
        self._url = f'{BASE_URL}{symbol}?p={symbol}'


    def get_price(self):
        r = requests.get(self._url, headers=HEADERS)

        if r.status_code != requests.codes.ok:
            return

        page_contents = html.fromstring(r.content)

        price_element = page_contents.xpath(
            '//*[@id="nimbus-app"]/section/section/section/article/section[1]/div[2]/div[1]/section/div/section[1]/div[1]/div[1]/span')

        if price_element:
            return price_element[0].text
        else:
            return None

