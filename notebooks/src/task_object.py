
class Task(object):

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<JigTask `{}`>'.format(self.name)

    @property
    def dependencies(self):
        return self.get('dependencies', [])

    @property
    def requires(self):
        return self.get('requires', [])

    def run(self):
        raise NotImplementedError()