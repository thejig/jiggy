"""Jiggy Runner methods."""
from importlib import import_module

from src.jiggy.inspector import Inspector
from src.jiggy.manager import Manager
from src.jiggy.pipeline import Pipeline
from src.jiggy.state import State
from src.jiggy.secrets import Secrets
from src.jiggy.task import Node


class Runner:
    """Executor base class for Jiggy."""

    def __init__(self, path: str):
        """Constructor for Runner."""
        self.path = path
        self.pipeline = Pipeline(path)
        self.dag = Manager(self.pipeline)

        for task in self.pipeline.tasks:
            self.dag.register_node(Node(task))

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
        for node_name in self.dag.associate():
            node = self.dag.library.get(node_name)
            pkg, mdl = self._parse_import(node.source)
            state, executed = self._execute(pkg=pkg, mdl=mdl, node=node, inputs=outputs)
            node.got = executed
            node.state = state

            print(node.got)

            outputs.update({node.name: node.got})
            self.state.append("Task: `{}` -> {}".format(node, state))

        return self.state

    @staticmethod
    def _parse_import(import_path):
        """Parse input source module to execute."""
        pkg = ".".join(import_path.split(".")[:-1])
        mdl = import_path.split(".")[-1]

        return pkg, mdl

    @staticmethod
    def __cls_run(init_cls: getattr, arguments=None):
        """Initialize function wrapper with state tracking. -> raises Inspector"""
        try:
            if arguments:
                output = init_cls.run(*arguments)
            else:
                output = init_cls.run()
            state = State.SUCCESS
        except Exception as exc:
            print(exc)
            output = None
            state = State.FAILED

        return state, output

    def _execute(self, pkg: str, mdl: str, node: Node, inputs=None):
        """Recursive executor for finding *args and **kwargs."""
        arguments = []
        inspector = Inspector(node=node)

        cls = getattr(import_module(pkg), mdl)
        init_cls = cls(node.name)

        if node.params:
            for param in node.params:
                dependency = param.get("dependency")
                if dependency:
                    arguments.append(
                        inspector.inspect_param(
                            param=param, received=inputs.get(dependency)
                        )
                    )
                elif not dependency:
                    arguments.append(
                        inspector.inspect_param(
                            param=param, received=param.get("value")
                        )
                    )

        state, output = self.__cls_run(init_cls=init_cls, arguments=arguments)

        return state, inspector.inspect_output(node=node, fout=output)

    def run(self):
        """Abstract runner for Sequential."""
        return self.main()


if __name__ == "__main__":
    myrun = SequentialRunner(path="examples/inputs/new_ext.yml").run()

    import pdb

    pdb.set_trace()
