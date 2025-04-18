import requests
from bs4 import BeautifulSoup


class WikiWorker(object):
    def __init__(self):
        self._url = 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'


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


