import threading
import time
from workers.WikiWorker import WikiWorker
from workers.YahooFinanceWorkerV2 import YahooFinancePriceScheduler
from workers.PostgresWorker import PostgresScheduler
from multiprocessing import Queue
from utils.logging_functions import logger

def main():
    scrapper_start_time = time.time()
    symbol_queue = Queue() # queues are threadsafe
    postgres_queue = Queue()

    number_of_threads = 10

    yahoo_finance_workers = []
    for i in range(number_of_threads):
        yahoo_finance_price_scheduler = YahooFinancePriceScheduler(input_queue=symbol_queue, output_queue=postgres_queue)
        yahoo_finance_workers.append(yahoo_finance_price_scheduler)

    postgres_workers = []
    for i in range(number_of_threads):
        postgres_worker = PostgresScheduler(input_queue=postgres_queue)
        postgres_workers.append(postgres_worker)

    wiki_worker = WikiWorker()
    for symbol in wiki_worker.get_sp_500_companies():
        symbol_queue.put(symbol)

    for i in range(len(yahoo_finance_workers)):
        symbol_queue.put("DONE")

    # Join YahooFinance Workers first
    for i in range(len(yahoo_finance_workers)):
        yahoo_finance_workers[i].join()

    # Now send "DONE" to Postgres workers
    for i in range(len(postgres_workers)):
        postgres_queue.put("DONE")

    # Join Postgres Workers
    for i in range(len(postgres_workers)):
        postgres_workers[i].join()


    logger.info(f"Finished. Extracting price took {time.time() - scrapper_start_time} seconds")

if __name__ == "__main__":
    main()


# V2
# def main():
#     symbol_queue = Queue() # queues are threadsafe
#     scrapper_start_time = time.time()
#
#     wiki_worker = WikiWorker()
#     current_workers = []
#     number_of_threads = 10
#
#     for i in range(number_of_threads):
#         yahoo_finance_price_scheduler = YahooFinancePriceScheduler(input_queue=symbol_queue)
#         current_workers.append(yahoo_finance_price_scheduler)
#
#     for symbol in wiki_worker.get_sp_500_companies():
#         symbol_queue.put(symbol)
#
#     for i in range(len(current_workers)):
#         symbol_queue.put("DONE")
#
#     for i in range(len(current_workers)):
#         current_workers[i].join()
#
#
#     print(f"Extracting price took {time.time() - scrapper_start_time} seconds")
#




# V1
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
