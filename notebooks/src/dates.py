import datetime
from notebooks.src.task_object import Task


class GetDateTask(Task):
    def __init__(self, name):
        self.name = name
        super(GetDateTask, self).__init__(name)
    def run(self):
        return datetime.datetime.now()

class GetWeekdayTask(Task):
    def __init__(self, name):
        self.name = name
        super(GetWeekdayTask, self).__init__(name)
    def run(self, x):
        return x.strftime('%A')

class GetFirstLetter(Task):
    def __init__(self, name):
        self.name = name
        super(GetFirstLetter, self).__init__(name)
    def run(self, x):
        return x[0]