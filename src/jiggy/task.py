from typing import Union

class Task(dict):
    """Task Object for initializer."""

    def __init__(self, name):
        self.name = name
        super(Task, self).__init__(name)

    def __repr__(self):
        return "<Task `{}`>".format(self.name)

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
    def source(self) -> str:
        function = self.function
        return function.get("source", None) if function else None

    @property
    def params(self) -> Union[list, None]:
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

    def run(self, *args):
        raise NotImplementedError()