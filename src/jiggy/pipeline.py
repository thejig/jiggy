"""Parser for input YAML."""
from typing import Union

import yaml


class Pipeline(object):
    """Create facade object with accesses."""

    def __init__(self, path: str):
        self.config = self._read(path=path)

    def __repr__(self):
        return "<Pipeline `{}`>".format(self.name)

    @property
    def name(self) -> Union[str, None]:
        """Top level pipeline name."""
        return self.config.get("name", None)

    @property
    def author(self) -> Union[str, None]:
        """Top level pipeline author."""
        return self.config.get("author", None)

    @property
    def version(self) -> Union[str, None]:
        """Top level pipeline author."""
        return self.config.get("version", None)

    @property
    def description(self) -> Union[str, None]:
        """Top level pipeline description."""
        return self.config.get("description", None)

    @property
    def info(self) -> dict:
        """Pipeline object in yaml."""
        return self.config.get("pipeline", {}) if self else None

    @property
    def runner(self) -> str:
        """Pipeline executor type."""
        return self.info.get("runner", "sequential") if self.info else None

    @property
    def secrets(self) -> Union[str, None]:
        """Pipeline secrets configiguration."""
        return self.info.get("secrets", None) if self.info else None

    @property
    def tasks(self) -> list:
        """Task objects in yaml."""
        return self.info.get("tasks", []) if self.info else None

    @staticmethod
    def _read(path: str):
        """Reader of .yml file."""
        with open(path, 'r') as f:
            return yaml.full_load(f)
