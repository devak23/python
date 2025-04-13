import time
from workers.WikiWorker import WikiWorker
from workers.YahooFinanceWorker import YahooFinanceWorker

def main():
    current_workers = []
    scrapper_start_time = time.time()

    wiki_worker = WikiWorker()
    for symbol in wiki_worker.get_sp_500_companies():
        yahoo_finance_worker = YahooFinanceWorker(symbol=symbol)
        current_workers.append(yahoo_finance_worker)

    for t in current_workers:
        t.join()

    print(f"Extracting price took {time.time() - scrapper_start_time} seconds")


if __name__ == "__main__":
    main()