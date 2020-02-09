import json
from importlib import import_module
from typing import Union

import dotenv
import yaml
from pathlib import Path


# TODO: make a `JiggyException` superclass and `NotFoundError` a subclass
class JiggySecretsError(Exception):
    pass


class Secrets:
    """Class handling secrets"""

    def __init__(self, path: str):
        self._path = self._check_valid(path=path)

    def __repr__(self):
        return "<Secrets `{path}`>".format(path=self._path)

    @property
    def path(self):
        return self._path

    @staticmethod
    def _check_valid(path: str) -> Union[Path, JiggySecretsError]:
        """Checks validity of secrets configuration path provided.

        Args:
            path (str): String representation of secrets configuration path

        Raises:
            JiggySecretsError (Exception): if the secrets filepath does not
                exist or is not a file

        Returns:
            path (pathlib.Path): PosixPath of validated secrets configuration
                path
        """

        path = Path(path)

        if not path.exists():
            raise JiggySecretsError("secrets configuration path does not exist")

        if not path.is_file():
            raise JiggySecretsError("secrets configuration must be a file")

        return path

    def load(self) -> dict:
        raise NotImplementedError("`load` must be implemented in subclass")


class EnvSecrets(Secrets):
    """Sublass of ``Secrets`` handling `.env` based secrets"""

    def __init__(self, path: str):
        super(EnvSecrets, self).__init__(path)

    def __repr__(self):
        return "<EnvSecrets `{path}`>".format(path=self.path)

    def load(self) -> dict:
        """Returns a dictionary containing all secrets"""
        secrets = dotenv.main.dotenv_values(dotenv_path=self.path)
        return secrets


class JSONSecrets(Secrets):
    """Sublass of ``Secrets`` handling `JSON` based secrets"""

    def __init__(self, path: str):
        super(JSONSecrets, self).__init__(path)

    def __repr__(self):
        return "<JSONSecrets `{path}`>".format(path=self.path)

    def load(self) -> dict:
        """Returns a dictionary containing all secrets"""
        secrets = json.load(open(self.path, "r"))
        return secrets


class YAMLSecrets(Secrets):
    """Sublass of ``Secrets`` handling `YAML` based secrets"""

    def __init__(self, path: str):
        super(YAMLSecrets, self).__init__(path)

    def __repr__(self):
        return "<YAMLSecrets `{path}`>".format(path=self.path)

    def load(self) -> dict:
        """Returns a dictionary containing all secrets"""
        secrets = yaml.load(open(self.path, "r"))
        return secrets
