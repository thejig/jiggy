"""Create JAG Object."""
from itertools import chain

from typing import Any

from src.jiggy.pipeline import Pipeline
from src.jiggy.task import JigTask


class Manager(object):
    """DAG creation/association mechanism."""

    def __init__(self, pipeline: Pipeline):
        self._pipeline = pipeline

    def associate(self) -> tuple:
        """Associate dependencies and tasks for order."""
        jdag = []
        for task in self._pipeline.tasks:
            insertion = self.parse_dependencies(jdag=jdag, current=task)

            jdag.insert(insertion, JigTask(task))

        in_place_tasks = jdag[::-1]

        return tuple([task for task in in_place_tasks])

    def parse_dependencies(self, jdag: list, current: dict) -> int:
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
