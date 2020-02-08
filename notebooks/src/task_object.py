
class Task(object):

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<JigTask `{}`>'.format(self.name)

    def run(self):
        raise NotImplementedError()