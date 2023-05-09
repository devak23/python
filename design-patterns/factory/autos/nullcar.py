from .abs_auto import AbsAuto


class NullCar(AbsAuto):
    def __init__(self, car):
        self.__car = car

    def start(self):
        print(f'Cannot start {self.__car}. Unknown Car!')

    def stop(self):
        pass
