import time
from workers.WikiWorker import WikiWorker
from workers.YahooFinanceWorkerV2 import YahooFinancePriceScheduler
from multiprocessing import Queue

def main():
    symbol_queue = Queue() # queues are threadsafe
    scrapper_start_time = time.time()

    wiki_worker = WikiWorker()
    current_workers = []
    number_of_threads = 4

    for i in range(number_of_threads):
        yahoo_finance_price_scheduler = YahooFinancePriceScheduler(input_queue=symbol_queue)
        current_workers.append(yahoo_finance_price_scheduler)

    for symbol in wiki_worker.get_sp_500_companies():
        symbol_queue.put(symbol)

    for i in range(len(current_workers)):
        symbol_queue.put("DONE")

    for i in range(len(current_workers)):
        current_workers[i].join()


    print(f"Extracting price took {time.time() - scrapper_start_time} seconds")


if __name__ == "__main__":
    main()


# def main():
#     current_workers = []
#     calc_start_time = time.time()
#
#     wiki_worker = WikiWorker()
#     for symbol in wiki_worker.get_sp_500_companies():
#         yahoo_finance_worker = YahooFinanceWorker(symbol=symbol)
#         current_workers.append(yahoo_finance_worker)
#
#     for t in current_workers:
#         t.join()
#
#     print(f"calculate_sum_of_squares took {time.time() - calc_start_time} seconds")
#
#     current_workers = []
#     sleep_start_time = time.time()
#     for seconds in range(1, 6):
#         current_workers.append(sleepy_workers)
#
#     for t in current_workers:
#         t.join()
#
#     print(f"sleep_a_little took {time.time() - sleep_start_time} seconds")
