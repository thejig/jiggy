import datetime
from src.task_object import Task


class GetDateTask(Task):
    def __init__(self, name):
        self.name = name
        super(GetDateTask, self).__init__(name)
    def run(self):
        return datetime.datetime.now()