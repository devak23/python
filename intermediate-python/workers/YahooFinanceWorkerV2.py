import queue
import threading
import time
from datetime import datetime, timezone
from utils.logging_functions import logger

import requests
from lxml import html

BASE_URL = 'https://finance.yahoo.com/quote/'
HEADERS = {'User-Agent': "Mozilla/6.0 (X11; Ubuntu; Linux i586; rv:49.0) Gecko/20200202 Firefox/49.0"}

class YahooFinancePriceScheduler(threading.Thread):
    def __init__(self, input_queue, output_queues, **kwargs):
        super(YahooFinancePriceScheduler, self).__init__(name="Test1", **kwargs)
        self._input_queue = input_queue
        temp_queue = output_queues
        if type(temp_queue) != list:
            # we are expecting the output queue to be a list of queues. So we have the flexibility wherein we can save
            # to multiple databases.
            temp_queue = [temp_queue]
        self._output_queues = temp_queue
        self.start()

    def run(self):
        while True:
            try:
                val = self._input_queue.get(timeout=10) # blocking call
            except queue.Empty:
                logger.error("Yahoo scheduler timing out. Stopping.")
                break

            if val == 'DONE':
                break
            else:
                yahoo_finance_price_worker = YahooFinanceWorkerV2(symbol=val)
                text_price = yahoo_finance_price_worker.get_price()
                price = float(text_price.replace(',', '')) if text_price else None
                for output_queue in self._output_queues:
                    output_values = (val, price, datetime.now(timezone.utc))
                    output_queue.put(output_values)



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

