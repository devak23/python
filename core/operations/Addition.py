from core.operations.Command import Command


class Addition(Command):

    def __init__(self, number1, number2):
        self._n1 = number1
        self._n2 = number2

    def execute(self):
        return self._n1 + self._n2
