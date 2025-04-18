import os
import threading
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import text
from utils.logging_functions import logger
from queue import Empty

INSERT_QUERY = """INSERT INTO prices (symbol, price, extracted_time) VALUES (:symbol, :price, :extracted_time)"""

PG_USER = os.environ.get('PG_USER') or 'postgres'
PG_PASS = os.environ.get('PG_PASS') or ''
PG_HOST = os.environ.get('PG_HOST') or 'localhost'
PG_PORT = os.environ.get('PG_PORT') or '5432'
PG_DB = os.environ.get('PG_DB') or 'postgres'

DB_URL = f'postgresql://{PG_USER}:{PG_PASS}@{PG_HOST}:{PG_PORT}/{PG_DB}'

ENGINE = create_engine(
    DB_URL,
    pool_size=10,
    max_overflow=5,
    pool_timeout=30,
    pool_recycle=1800
)

# Create a session factory bound to the engine
Session = sessionmaker(bind=ENGINE, autoflush=True)


class PostgresScheduler(threading.Thread):
    def __init__(self, input_queue, **kwargs):
        super(PostgresScheduler, self).__init__(**kwargs)
        self._input_queue = input_queue
        self.start()
        self._session = Session()

    def run(self):
        while True:
            try:
                val = self._input_queue.get(timeout=10)  # blocking call
                if val == 'DONE':
                    self._session.close()
                    break
                else:
                    symbol, price, extracted_time = val
                    postgres_worker = PostgresWorker(self._session, symbol, price, extracted_time)
                    postgres_worker.insert_into_db()
            except Empty:
                logger.error("Timeout reached in the postgres scheduler. Stopping.")
                break
            except Exception as e:
                logger.error("ERROR encountered while inserting into db", e)
                self._session.close()


class PostgresWorker:
    def __init__(self, session, symbol, price, extracted_time):
        self._session = session
        self._symbol = symbol
        self._price = price
        self._extracted_time = extracted_time

    def insert_into_db(self):
        # logger.info(f"executing query: {INSERT_QUERY}, params: {self._symbol}, {self._price}, {self._extracted_time}")
        self._session.execute(text(INSERT_QUERY), {'symbol': self._symbol
            , 'price': self._price
            , 'extracted_time': self._extracted_time
                                                   })
        self._session.commit()
