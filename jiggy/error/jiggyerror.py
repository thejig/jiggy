"""Jiggy Error Library."""


class JiggyError(Exception):
    """JIggyError Base Class."""

    pass


class JiggyPlaybookError(JiggyError):
    """JiggyPlayBook (jpl) Error Delegation."""

    def __init__(self, jpl_errors: list) -> None:
        """Constructor for JiggyPlaybookError."""
        self.errors = jpl_errors

    def __str__(self):
        """Thrown exception error info."""
        for error in self.errors:
            print(error.message)

        return "Error(s) found in Jiggy Playbook"


class InspectorParamException(JiggyError):
    """Inspector Exception for param type mismatch."""

    def __init__(self, node, received, expected):
        """Constructor for InspectorParamException."""
        self.node = node
        self.received = received
        self.expected = expected

    def __str__(self):
        """Thrown exception error info."""
        return "{} parameter: {} does not match declared type: {}".format(
            self.node, self.received, self.expected
        )


class InspectorOutputException(JiggyError):
    """Inspector Exception for output type mismatch."""

    def __init__(self, node, received, expected):
        """Constructor for InspectorOutputException."""
        self.node = node
        self.received = received
        self.expected = expected

    def __str__(self):
        return "{} function output: {} does not match declared type: {}".format(
            self.node, self.received, self.expected
        )


__all__ = [
    JiggyError,
    JiggyPlaybookError,
    InspectorParamException,
    InspectorOutputException,
]
