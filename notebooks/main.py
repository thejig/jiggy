from notebooks.src.jag import Jag
from importlib import import_module


def main(fp):  # for the sake of brevity
    jag = Jag(fp).associate

    _outputs = []

    for jtask in jag:
        package, module = parse_module(jtask.source)

        executed = _execute(
            package=package,
            module=module,
            jtask=jtask,
            inputs=_outputs
        )

        _outputs.append(
            {jtask.name: executed}
        )

    return 'Done!'


def parse_module(module_path):
    package = '.'.join(module_path.split('.')[:-1])
    module = module_path.split('.')[-1]

    return package, module


def _execute(
        package, module, jtask, *args, inputs=None, **kwargs
):
    """.."""
    argument=None

    cls = getattr(import_module(package), module)
    init_cls = cls(jtask.name)

    if jtask.dependencies and inputs:
        for pinputs in inputs:
            if pinputs.get(jtask.dependencies[0]):
                argument = pinputs.get(jtask.dependencies[0])
            else:
                continue

    if argument:
        output = init_cls.run(argument)
    else:
        output = init_cls.run()

    print(output)

    return output


if __name__ == "__main__":
    main("notebooks/no_ext.yml")

    import pdb; pdb.set_trace()