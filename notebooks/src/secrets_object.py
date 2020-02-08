import json
from importlib import import_module
from typing import Union

import dotenv
import yaml
from pathlib import Path


# TODO: make a `JiggyException` superclass and `NotFoundError` a subclass
class JiggySecretsError(Exception):
    pass


class JiggySecrets:
    """Class handling secrets"""
    def __init__(self, path: str):
        self._path = self._check_valid(path=path)

    def __repr__(self):
        return '<JiggySecrets `{path}`>'.format(path=self._path)

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
            raise JiggySecretsError('secrets configuration path does not exist')

        if not path.is_file():
            raise JiggySecretsError('secrets configuration must be a file')

        return path

    def load(self) -> dict:
        raise NotImplementedError()


class EnvSecrets(JiggySecrets):
    """Sublass of ``Secrets`` handling `.env` based secrets"""
    def __init__(self, path: str):
        super(EnvSecrets, self).__init__(path)

    def __repr__(self):
        return '<EnvSecrets `{path}`>'.format(path=self.path)

    def load(self) -> dict:
        """Returns a dictionary containing all secrets"""
        secrets = dotenv.main.dotenv_values(dotenv_path=self.path)
        return secrets


class JSONSecrets(JiggySecrets):
    """Sublass of ``Secrets`` handling `JSON` based secrets"""
    def __init__(self, path: str):
        super(JSONSecrets, self).__init__(path)

    def __repr__(self):
        return '<JSONSecrets `{path}`>'.format(path=self.path)

    def load(self) -> dict:
        """Returns a dictionary containing all secrets"""
        secrets = json.load(open(self.path, 'r'))
        return secrets


class YAMLSecrets(JiggySecrets):
    """Sublass of ``Secrets`` handling `YAML` based secrets"""
    def __init__(self, path: str):
        super(YAMLSecrets, self).__init__(path)

    def __repr__(self):
        return '<YAMLSecrets `{path}`>'.format(path=self.path)

    def load(self) -> dict:
        """Returns a dictionary containing all secrets"""
        secrets = yaml.load(open(self.path, 'r'))
        return secrets


# class PySecrets(JiggySecrets):
#     """Sublass of ``Secrets`` handling `Python` based secrets"""
#     def __init__(self, path: str):
#         super(PySecrets, self).__init__(path)

#     def __repr__(self):
#         return '<PySecrets `{path}`>'.format(path=self.path)

#     @staticmethod
#     def _parse_module(path) -> dict:
#         """Returns a dictionary containing `package` and `module` import"""
#         import_path = str(path)
#         package = '.'.join(import_path.split('/')[:-1])
#         module = import_path.split('/')[-1].split('.')[0]
#         return package, module

#     def load(self) -> dict:
#         """Returns a dictionary containing all secrets"""
#         package, module = self._parse_module(self.path)
#         mdl = getattr(import_module(imports['package']), imports['module'])
#         import ipdb; ipdb.set_trace()