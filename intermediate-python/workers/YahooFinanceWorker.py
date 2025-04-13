import threading
import requests
from lxml import html

BASE_URL = 'https://finance.yahoo.com/quote/'


class YahooFinanceWorker(threading.Thread):
    def __init__(self, symbol, **kwargs):
        super(YahooFinanceWorker, self).__init__(**kwargs)
        self._symbol = symbol
        self._url = f'{BASE_URL}{symbol}'
        self.start()


    def run(self):
        r = requests.get('https://finance.yahoo.com/quote/APPL')
        page_contents = html.fromstring(r.text)
        price = page_contents.xpath('//*[@id="nimbus-app"]/section/section/section/article/section[1]/div[2]/div[1]/section/div/section[1]/div[1]/div[1]/span')
        print(price)


