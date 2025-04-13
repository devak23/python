import threading

class SquaredSumWorkers(threading.Thread):
    def __init__(self, n, **kwargs):
        self._n = n
        super(SquaredSumWorkers, self).__init__()
        self.start()


    def _calculate_sum_of_squares(self):
        sum_of_squares = 0
        for i in range(self._n):
            sum_of_squares += i ** 2

        print(sum_of_squares)

    def run(self):
        self._calculate_sum_of_squares()
