from src.jiggy.task import Task


class LowerText(Task):
    def __init__(self, name):
        self._name = name
        super(LowerText, self).__init__(name)

    def run(self, x, y):
        return f'{x}_+_{y}'.lower()


class PrintThis(Task):
    def __init__(self, name):
        self._name = name
        super(PrintThis, self).__init__(name)

    def run(self, x):
        print(x)