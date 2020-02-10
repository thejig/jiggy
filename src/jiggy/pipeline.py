"""Parser for input YAML."""
from typing import Union

import yaml


class Pipeline(object):
    """Create facade object with accesses."""

    def __init__(self, location: str):
        self.yaml = self._read_yaml(location=location)

    @property
    def name(self) -> Union[str, None]:
        """Top level pipeline name."""
        return self.yaml.get("name", None)

    @property
    def author(self) -> Union[str, None]:
        """Top level pipeline author."""
        return self.yaml.get("author", None)

    @property
    def version(self) -> Union[str, None]:
        """Top level pipeline author."""
        return self.yaml.get("version", None)

    @property
    def description(self) -> Union[str, None]:
        """Top level pipeline description."""
        return self.yaml.get("description", None)

    @property
    def pipeline(self) -> dict:
        """Pipeline object in yaml."""
        return self.yaml.get("pipeline", {}) if self else None

    @property
    def executor(self) -> str:
        """Pipeline executor type."""
        pipeline = self.pipeline
        return pipeline.get("executor", "sequential")

    @property
    def secrets(self) -> Union[str, None]:
        """Pipeline secrets configuration."""
        pipeline = self.pipeline
        return pipeline.get("secrets", None)

    @property
    def tasks(self) -> list:
        """Task objects in yaml."""
        pipeline = self.pipeline
        return pipeline.get("tasks", []) if pipeline else None

    @staticmethod
    def _read_yaml(location: str):
        """Reader of .yml file."""
        with open(location) as in_yaml:
            return yaml.full_load(in_yaml)
