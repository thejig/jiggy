"""Jiggy Runner methods."""
from importlib import import_module

from src.jiggy.manager import Manager
from src.jiggy.task import Node
from src.jiggy.pipeline import Pipeline
from src.jiggy.state import State
from src.jiggy.secrets import (

)

class Runner:
    """Executor base class for Jiggy."""

    def __init__(self, path: str):
        """Constructor for Runner."""
        self.pipeline = Pipeline(path)
        self.dag = Manager(self.pipeline)
        self.secrets = Secrets(self.pipeline)
        self.state = []

    def __repr__(self):
        """Repr method."""
        return "<Runner `{}`>".format(self.path)

    def run(self):
        """Abstract base class runner."""
        raise NotImplementedError()


class SequentialRunner(Runner):
    """Subclass of Runner for running a sequential pipeline."""

    def __init__(self, path: str):
        """Constructor for Sequential Runner."""
        super(SequentialRunner, self).__init__(path)

    def __repr__(self):
        """Repr method."""
        return "<SequentialRunner `{}`>".format(self.pipeline.name)

    def main(self):
        """Runner for Jiggy Pipeline."""

        outputs = {}

        for node in self.dag.order:
            pkg, mdl = self._parse_import(node.source)

            state, executed = self._execute(
                pkg=pkg,
                mdl=mdl,
                node=node,
                inputs=outputs,
            )

            outputs.update({node.name: executed})
            self.state.append("Task: `{}` -> {}".format(node.name, state))

        return self.state

    @staticmethod
    def _parse_import(import_path):
        """Parse input source module to execute."""
        pkg = ".".join(import_path.split(".")[:-1])
        mdl = import_path.split(".")[-1]

        return pkg, mdl

    @staticmethod
    def __cls_run(init_cls: getattr, arguments=None):
        """Initialize function wrapper with state tracking."""
        state = State.PENDING
        try:
            if arguments:
                output = init_cls.run(*arguments)
            else:
                output = init_cls.run()
            state = State.SUCCESS
        except Exception:
            output = None
            state = State.FAILED

        return state, output

    def _execute(
        self,
        pkg: str,
        mdl: str,
        node: Node,
        inputs=None
    ):
        """Recursive executor for finding *args and **kwargs."""
        arguments = []
        cls = getattr(import_module(pkg), mdl)
        init_cls = cls(node.name)

        if node.dependencies and inputs:
            for input_id in inputs.keys():
                if input_id in node.dependencies:
                    arguments.append(inputs[input_id])
                else:
                    continue

        state, output = self.__cls_run(init_cls=init_cls, arguments=arguments)

        return state, output

    def run(self):
        """Abstract runner for Sequential."""
        return self.main()
