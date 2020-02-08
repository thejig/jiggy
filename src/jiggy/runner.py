from importlib import import_module

from src.jiggy.manager import Manager
from src.jiggy.state import State
from src.jiggy.task import JagTask

from typing import Any


class Runner:
    """Executor base class for Jiggy."""

    def __init__(self, path: str):
        """Constructor for Runner."""
        self.path = path
        self.jag = Manager(path)
        self.pipeline_state = []

    def __repr__(self):
        """Repr method."""
        return "<Runner `{}`>".format(self.path)

    def load(self):
        raise NotImplementedError()


class SequentialRunner(Runner):
    """Subclass of Runner for running a sequential pipeline."""

    def __init__(self, path: str):
        """Constructor for Sequential Runner."""
        super(SequentialRunner, self).__init__(path)

    def __repr__(self):
        """Repr method."""
        return "<SequentialRunner `{}`>".format(self.path)

    def main(self):
        """Runner for Jiggy Pipeline."""
        jag = self.jag.associate

        _outputs = []

        for jtask in jag:
            jag_package, jag_module = self.parse_module(jtask.source)

            state, executed = self._execute(
                jag_package=jag_package,
                jag_module=jag_module,
                jtask=jtask,
                inputs=_outputs,
            )

            _outputs.append({jtask.name: executed})
            self.pipeline_state.append("<{}, {}>".format(jtask, state))

        return self.pipeline_state

    @staticmethod
    def parse_module(module_path):
        """Parse input source module to execute."""
        jag_package = ".".join(module_path.split(".")[:-1])
        jag_module = module_path.split(".")[-1]

        return jag_package, jag_module

    @staticmethod
    def __cls_run(init_cls: getattr, argument=None):
        """Initialize function wrapper with state tracking."""
        state = State.PENDING
        try:
            if argument:
                output = init_cls.run(argument)
            else:
                output = init_cls.run()
            state = State.SUCCESS
        except Exception:
            output = None
            state = State.FAILED

        return state, output

    def _execute(
        self,
        jag_package: str,
        jag_module: str,
        jtask: JagTask,
        *args: Any,
        inputs=None,
        **kwargs: Any
    ):
        """Recursive executor for finding *args and **kwargs."""
        argument = None
        cls = getattr(import_module(jag_package), jag_module)
        init_cls = cls(jtask.name)

        if jtask.dependencies and inputs:
            for pinputs in inputs:
                if pinputs.get(jtask.dependencies[0]):
                    argument = pinputs.get(jtask.dependencies[0])
                else:
                    continue

        state, output = self.__cls_run(init_cls=init_cls, argument=argument)

        return state, output

    def run(self):
        return self.main()
