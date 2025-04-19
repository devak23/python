from core.operations.Command import Command

class Subtraction(Command):
    def __init__(self, n1, n2):
        self._n1 = n1
        self._n2 = n2

    def execute(self):
        return self._n1 - self._n2