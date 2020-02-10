"""Create JAG Object."""
from itertools import chain

from typing import Any

from src.jiggy.pipeline import Pipeline
from src.jiggy.task import Node


class Manager(object):
    """DAG creation/association mechanism."""

    def __init__(self, pipeline: Pipeline):
        self.pipeline = pipeline

    def associate(self) -> tuple:
        """Associate dependencies and tasks for order."""

        dag = []
        for task in self.pipeline.tasks:
            insertion = self.parse_dependencies(dag=dag, current=task)
            dag.insert(insertion, Node(task))

        in_place_tasks = dag[::-1]

        return tuple([task for task in in_place_tasks])

    def parse_dependencies(self, dag: list, current: dict) -> int:
        """Check dependencies of existing task in JAG."""
        insertion = 0
        for idx, task in enumerate(dag):
            deps = self._add_if_instance(task.get("dependencies"))
            reqs = self._add_if_instance(task.get("requires"))

            _deps = chain(deps, reqs)
            if current.get("name") in _deps:
                insertion = idx + 1

        return insertion

    @staticmethod
    def _add_if_instance(arg: Any) -> list:
        """Create itertools.chain iterable"""
        arg_out = []
        if isinstance(arg, list):
            arg_out = arg

        return arg_out
