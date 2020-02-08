from dotenv import load_dotenv
from pathlib import Path


class JiggySecretsError(Exception):
    pass


class Secrets:
    """Class handling secrets"""
    def __init__(self, path: str):
        self.path = _check_valid(path=Path(path))

    def _check_valid(self, path: Path):
        if path.exists() and path.is_file():
            return path
        else:
            raise JiggySecretsError('unable to find secrets configuration path')
    
    def from_env():
        load_dotenv(dotenv_path=self.path)

    def from_yaml():

    def from_json():

    def from_pyfile():

    def config(self):
        """Abstraction for a secrets configuration class"""
        raise NotImplementedError()