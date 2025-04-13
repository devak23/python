import threading
import requests
from lxml import html

BASE_URL = 'http://finance.yahoo.com/quote/'
HEADERS = {}
HEADERS['User-Agent'] = "Mozilla/6.0 (X11; Ubuntu; Linux i586; rv:49.0) Gecko/20200202 Firefox/49.0"

class YahooFinanceWorker(threading.Thread):
    def __init__(self, symbol, **kwargs):
        super(YahooFinanceWorker, self).__init__(**kwargs)
        self._symbol = symbol
        self._url = f'{BASE_URL}{symbol}?p={symbol}'
        self.start()


    def run(self):
        print(f"url: {self._url}")
        r = requests.get(self._url, headers=HEADERS)
        page_contents = html.fromstring(r.content)
        price_element = page_contents.xpath(
            '//*[@id="nimbus-app"]/section/section/section/article/section[1]/div[2]/div[1]/section/div/section[1]/div[1]/div[1]/span')
        if price_element:
            print(f"price of {self._symbol} =  {price_element[0].text}")
        else:
            print(f"could not find price for {self._symbol}")

