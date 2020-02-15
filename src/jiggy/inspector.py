"""Inspector Module."""
import datetime  # noqa pylint: disable=unused-import

from src.jiggy.task import Node

from typing import Any


class InspectorParamException(Exception):
    """Inspector Exception for param type mismatch"""

    pass


class InspectorOutputException(Exception):
    """Inspector Exception for output type mismatch"""

    pass


class Inspector(object):
    """Inspector object for type clearing."""

    def __init__(self, node: Node):
        """Constructor for Inspector."""
        self._node = node

    def __repr__(self):
        """Representation of Inspector."""
        return "<Inspector {}>".format(self._node)

    def inspect_param(self, param: dict, received: Any):
        """Inspector helper for input and type."""
        if not isinstance(received, eval(param.get("type"))):
            raise InspectorParamException(
                "{} parameter: {} does not match declared type: {}".format(
                    self._node, received, param.get("type")
                )
            )

        return received

    def inspect_output(self, node: Node, fout: Any):
        """Inspector helper for output and type."""
        if not fout:
            return None

        if not isinstance(fout, eval(node.output.get("type"))):
            raise InspectorOutputException(
                "{} function output: {} does not match declared type: {}".format(
                    self._node, fout, node.output.get("type")
                )
            )

        return fout
