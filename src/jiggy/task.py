"""Jiggy Task and JigTask definitions."""
from typing import Union


class Node(dict):
    """Task Object for initializer."""

    foutput = None
    state = None

    def __init__(self, data):
        """Constructor for Node."""
        super(Node, self).__init__(data)

    def __repr__(self):
        """Representation of Node."""
        return "<Node `{}`>".format(self.name)

    @property
    def name(self) -> str:
        """Assign `task.name` property."""
        return self.get("name")

    @property
    def description(self) -> Union[str, None]:
        """Assign `task.description` property."""
        return self.get("description", None)

    @property
    def function(self) -> dict:
        """Assign `task.function` property."""
        return self.get("function", {})

    @property
    def source(self) -> str:
        """Assign `task.function.source` property."""
        function = self.function
        return function.get("source", None) if function else None

    @property
    def params(self) -> Union[list, None]:
        """Assign `task.function.params` property."""
        function = self.function
        return function.get("params", []) if function else None

    @property
    def output(self) -> dict:
        """Assign `task.output` property."""
        return self.get("output", {})

    @property
    def output_id(self) -> Union[list, None]:
        """Assign `task.output.id` property."""
        output = self.output
        return output.get("id", []) if output else None

    @property
    def output_type(self) -> Union[str, None]:
        """Assign `task.output.type` property."""
        output = self.output
        return output.get("type", None) if output else None

    @property
    def requires(self) -> list:
        """Assign `task.requires` property."""
        return self.get("requires", [])

    def run(self, *args):
        """Abstract runner for JigTask."""
        raise NotImplementedError()


class Task(object):
    """Base class for Task object."""

    def __init__(self, name):
        """Constructor for Task object."""
        self.name = name

    def __repr__(self):
        """Repr method."""
        return "<Task `{}`>".format(self.name)

    def run(self, *args):
        """Abstract runner for Task."""
        raise NotImplementedError()
