"""Create JAG Object."""
import yaml

from itertools import chain


class Jag(object):
    """DAG creation/association mechanism."""

    def __init__(self, location: str):
        self.location = location
        self.yaml = self.__read_yaml

    @property
    def associate(self) -> list:
        """Associate dependencies and tasks for order."""
        jdag = []
        for idx, task in enumerate(self.tasks):
            insertion = self._check_dependencies(jdag=jdag, current=task)

            jdag.insert(insertion, task)

        return jdag[::-1]

    @staticmethod
    def _check_dependencies(jdag: list, current: dict) -> int:
        """Check dependencies of existing task in JAG."""
        insertion = 0
        for jdag_idx, task in enumerate(jdag):

            # TODO `itertools.chain` depends on iterables for both vars
            # should we consider marshalling `requires` to be an array as well?

            """
            >>> chain([], None)
            >>> TypeError: argument of type 'NoneType' is not iterable
            
            >>> chain([], [])
            >>> <itertools.chain object at 0x10474f908>
            """

            _deps = chain(task.get("dependencies"), task.get("requires"))
            import pdb; pdb.set_trace()
            if current.get("name") in _deps:
                insertion = jdag_idx + 1

        return insertion

    @property
    def pipeline(self) -> dict:
        """Pipeline object in yaml."""
        return self.yaml.get("pipeline", {}) if self else None

    @property
    def tasks(self) -> dict:
        """Task objects in yaml."""
        pipeline = self.pipeline
        return pipeline.get("tasks", {}) if pipeline else None

    @property
    def __read_yaml(self):
        """Reader of .yml file."""
        with open(self.location) as in_yaml:
            return yaml.full_load(in_yaml)


if __name__ == '__main__':
    jag = Jag('notebooks/jag_ex.yml').associate
