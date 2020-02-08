from typing import Union

import dotenv
from pathlib import Path


# TODO: make a `JiggyException` superclass and `NotFoundError` a subclass
class JiggySecretsError(Exception):
    pass


class JiggySecrets:
    """Class handling secrets"""
    def __init__(self, path: str):
        self._path = self._check_valid(path=path)

    def __repr__(self):
        return '<JiggySecrets `{path}`, `{type}`>'.format(path=self._path)

    @property
    def path(self):
        return self._path

    @property
    def type(self):
        return self._type

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
            raise JiggySecretsError('secrets configuration does not exist')

        if not path.is_file():
            raise JiggySecretsError('secrets configuration must be a file')

        return path

    def load(self) -> dict:
        raise NotImplementedError()


class EnvSecrets(JiggySecrets):
    """Sublass of ``Secrets`` handling `.env` based secrets"""
    def __init__(self, path):
        super(EnvSecrets, self).__init__(path)

    def __repr__(self):
        return '<EnvSecrets `{path}`>'.format(path=self.path)

    def load(self) -> dict:
        secrets = dotenv.main.dotenv_values(dotenv_path=self.path)
        return secrets


    # def from_env(self) -> dict:
    #     load_dotenv(dotenv_path=self.path)
    #     import ipdb; ipdb.set_trace()

    # def from_yaml():
    #     pass

    # def from_json():
    #     pass

    # def from_pyfile():
    #     pass

    # def config(self):
    #     """Abstraction for a secrets configuration class"""
    #     raise NotImplementedError()