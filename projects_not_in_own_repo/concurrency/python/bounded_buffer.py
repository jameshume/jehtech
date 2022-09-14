import threading
import numpy as np
import time
import logging
import sys

class ExampleThreadSafeBoundedBuffer(object):
    def __init__(self, size, logger):
        self._size = size
        self._q = [None] * self._size
        self._start = 0
        self._end = 0
        self._elements = threading.Semaphore(0)
        self._spaces = threading.Semaphore(self._size)
        self._cr = threading.Lock()
        self._logger = logger
 
    def enqueue(self, item):
        # Wait for a space to become available
        self._spaces.acquire()
 
        # Enter a critical region. We require this because if there are
        # multiple writers we could have multiple threads executing this logic
        # so we must enforce mutual exclusion.
        with self._cr:
            self._logger.info(f"Enqueue {item}")
            self._q[self._end] = item
            self._end = (self._end + 1) % self._size
 
        # Signal anyone waiting for an element to become available...
        self._elements.release()
 
    def dequeue(self):
        item = None
        # Wait for an element to be available in the buffer
        self._elements.acquire()
 
        # Enter a critical region. We require this because if there are
        # multiple readers we could have multiple threads executing this logic
        # so we must enforce mutual exclusion.
        with self._cr:
            self._logger.info(f"Dequeue {self._q[self._start]}")
            item = self._q[self._start]
            self._start = (self._start + 1) % self._size
 
        # Signal anyone waiting for a space to become available...
        self._spaces.release()
        return item

class Producer(threading.Thread):
    def __init__(self, mean_production_time_seconds, queue, logger):
        super().__init__()
        self._mean_production_time_seconds = mean_production_time_seconds
        self._queue = queue
        self._logger = logger

    def run(self):
        counter = 0
        while True:
            self._logger.info(f"Produce {counter}")
            self._queue.enqueue(counter)
            counter += 1
            time.sleep(abs(np.random.default_rng().normal(self._mean_production_time_seconds)))

class Consumer(threading.Thread):
    def __init__(self, mean_consumption_time_seconds, queue, logger):
        super().__init__()
        self._mean_consumption_time_seconds = mean_consumption_time_seconds
        self._queue = queue
        self._logger = logger

    def run(self):
        while True:
            value = self._queue.dequeue()
            self._logger.info(f"Consumed {value}")
            time.sleep(abs(np.random.default_rng().normal(self._mean_consumption_time_seconds)))


if __name__ == '__main__':
    logger = logging.getLogger(__name__) 
    logger.setLevel(logging.INFO)
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    queue = ExampleThreadSafeBoundedBuffer(3, logger)
    producer = Producer(1, queue, logger)
    consumer = Consumer(2, queue, logger)

    consumer.start()
    producer.start()

    consumer.join()
    producer.join()
