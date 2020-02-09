"""Jiggy Runner methods."""
from importlib import import_module

from src.jiggy.manager import Manager
from src.jiggy.pipeline import Pipeline
from src.jiggy.state import State
from src.jiggy.task import JigTask


class Runner:
    """Executor base class for Jiggy."""

    def __init__(self, path: str):
        """Constructor for Runner."""
        self.path = path
        self._pipeline = Pipeline(path)
        self.jag = Manager(self._pipeline)
        self.pipeline_state = []

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
        return "<SequentialRunner `{}`>".format(self.path)

    def main(self):
        """Runner for Jiggy Pipeline."""
        jiggy_dag = self.jag.associate()

        _outputs = []

        for jig_task in jiggy_dag:
            jig_package, jig_module = self.parse_module(jig_task.source)

            state, executed = self._execute(
                jig_package=jig_package,
                jig_module=jig_module,
                jtask=jig_task,
                inputs=_outputs,
            )

            _outputs.append({jig_task.name: executed})
            self.pipeline_state.append("<{}, {}>".format(jig_task, state))

        return self.pipeline_state

    @staticmethod
    def parse_module(module_path):
        """Parse input source module to execute."""
        jig_package = ".".join(module_path.split(".")[:-1])
        jig_module = module_path.split(".")[-1]

        return jig_package, jig_module

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
            jig_package: str,
            jig_module: str,
            jtask: JigTask,
            inputs=None
    ):
        """Recursive executor for finding *args and **kwargs."""
        argument = None
        cls = getattr(import_module(jig_package), jig_module)
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
        """Abstract runner for Sequential."""
        return self.main()
