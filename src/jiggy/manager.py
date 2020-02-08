"""Create JAG Object."""
import yaml

from itertools import chain

from typing import Any, Union


class Manager(object):
    """DAG creation/association mechanism."""

    def __init__(self, location: str):
        self.location = location
        self.yaml = self.__read_yaml()

    @property
    def associate(self) -> tuple:
        """Associate dependencies and tasks for order."""
        jdag = []
        for idx, task in enumerate(self.tasks):
            insertion = self._check_dependencies(jdag=jdag, current=task)

            jdag.insert(insertion, JagTask(task))

        in_place = jdag[::-1]

        return tuple([x for x in in_place])

    def _check_dependencies(self, jdag: list, current: dict) -> int:
        """Check dependencies of existing task in JAG."""
        insertion = 0
        for jdag_idx, task in enumerate(jdag):

            deps = self._add_if_instance(task.get("dependencies"))
            reqs = self._add_if_instance(task.get("requires"))

            _deps = chain(deps, reqs)
            if current.get("name") in _deps:
                insertion = jdag_idx + 1

        return insertion

    @staticmethod
    def _add_if_instance(arg: Any) -> list:
        """Create itertools.chain iterable"""
        arg_out = []
        if isinstance(arg, list):
            arg_out = arg

        return arg_out

    @property
    def name(self) -> Union[str, None]:
        """Top level pipeline name."""
        return self.yaml.get('name', None)

    @property
    def author(self) -> Union[str, None]:
        """Top level pipeline author."""
        return self.yaml.get('author', None)

    @property
    def version(self) -> Union[str, None]:
        """Top level pipeline author."""
        return self.yaml.get('version', None)

    @property
    def description(self):
        """Top level pipeline description."""
        return self.yaml.get('description', None)

    @property
    def pipeline(self) -> dict:
        """Pipeline object in yaml."""
        return self.yaml.get("pipeline", {}) if self else None

    @property
    def executor(self) -> str:
        pipeline = self.pipeline
        return pipeline.get('executor', 'sequential')

    @property
    def secrets(self) -> Union[str, None]:
        pipeline = self.pipeline
        return pipeline.get('secrets', None)

    @property
    def tasks(self) -> dict:
        """Task objects in yaml."""
        pipeline = self.pipeline
        return pipeline.get("tasks", {}) if pipeline else None

    def __read_yaml(self):
        """Reader of .yml file."""
        with open(self.location) as in_yaml:
            return yaml.full_load(in_yaml)
