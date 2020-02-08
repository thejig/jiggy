"""Create JAG Object."""
import yaml

from itertools import chain

from typing import Union


class Jag(object):
    """DAG creation/association mechanism."""

    def __init__(self, location: str):
        self.location = location
        self.yaml = self.__read_yaml

    @property
    def associate(self) -> tuple:
        """Associate dependencies and tasks for order."""
        jdag = []
        for idx, task in enumerate(self.tasks):
            insertion = self._check_dependencies(jdag=jdag, current=task)

            jdag.insert(insertion, Task(task))

        return tuple([x for x in jdag[::-1]])

    def _check_dependencies(self, jdag: list, current: dict) -> int:
        """Check dependencies of existing task in JAG."""
        insertion = 0
        for jdag_idx, task in enumerate(jdag):

            all_deps = self._add_if_instance(
                task.get("dependencies"), task.get("requires")
            )

            _deps = chain(all_deps)
            if current.get("name") in _deps:
                insertion = jdag_idx + 1

        return insertion

    @staticmethod
    def _add_if_instance(*args) -> list:
        """Create itertools.chain iterable"""
        arg_out = []
        for arg in args:
            if isinstance(arg, list):
                arg_out.append(arg)

        return arg_out

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


class Task(dict):
    def __init__(self, task):
        super(Task, self).__init__(task)

    def __repr__(self):
        return "<JigTask `{}`>".format(self.name)

    @property
    def name(self) -> str:
        return self.get("name")

    @property
    def description(self) -> Union[str, None]:
        return self.get("description", None)

    @property
    def function(self) -> dict:
        return self.get("function", {})

    @property
    def source(self) -> Union[str, None]:
        function = self.function
        return function.get("source", None) if function else None

    @property
    def source(self) -> Union[str, None]:
        function = self.function
        return function.get("params", None) if function else None

    @property
    def output(self) -> dict:
        return self.get("output", {})

    @property
    def id(self) -> Union[list, None]:
        output = self.output
        return output.get("id", []) if output else None

    @property
    def type(self) -> Union[str, None]:
        output = self.output
        return output.get("type", None) if output else None

    @property
    def dependencies(self) -> list:
        return self.get("dependencies", [])

    @property
    def requires(self) -> list:
        return self.get("requires", [])

    def run(self):
        raise NotImplementedError()


if __name__ == "__main__":
    jag = Jag("notebooks/jag_ex.yml").associate
