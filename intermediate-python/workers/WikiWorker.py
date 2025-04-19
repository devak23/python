import threading

import requests
from bs4 import BeautifulSoup


class WikiWorkerScheduler(threading.Thread):
    def __init__(self, output_queues, **kwargs):
        if 'input_queues' in kwargs:
            kwargs.pop('input_queues')

        self._entries = kwargs.pop('input_values')
        super(WikiWorkerScheduler, self).__init__(**kwargs)
        self._output_queues = output_queues
        self.start()


    def run(self):
        for entry in self._entries:
            wiki_worker = WikiWorker(entry)
            for symbol in wiki_worker.get_sp_500_companies():
                for output_queue in self._output_queues:
                    output_queue.put(symbol)

        for output_queue in self._output_queues:
            output_queue.put("DONE")


class WikiWorker(object):
    def __init__(self, url):
        self._url = url


    @staticmethod
    def _extract_company_symbols(page_html):
        soup = BeautifulSoup(page_html, 'lxml')
        table = soup.find(id="constituents")
        table_rows = table.find_all("tr")

        for tr in table_rows[1:]:
            symbol = tr.find('td').text.strip('\n')
            yield symbol


    def get_sp_500_companies_alternate(self):
        symbols = ['MSFT','GOOG','AAPL']
        for i in range(len(symbols)):
            yield symbols[i]


    def get_sp_500_companies(self):
        response = requests.get(self._url)
        if response.status_code != 200:
            print("Couldn't get entries")
            return []

        yield from self._extract_company_symbols(response.content)


