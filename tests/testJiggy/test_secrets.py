"""Test Manager Classes."""
from unittest import TestCase

from jiggy.pipeline import Pipeline
from jiggy.secrets import Secrets


class TestEnvSecrets(TestCase):
    """Test suite for src.jiggy.manager."""

    def __init__(self, path):
        """Construct TestCase."""
        test_pipeline = Pipeline(path="testData/minimal_test_case.yml")
        self.test_secrets = Secrets(pipeline=test_pipeline)
        super(TestEnvSecrets, self).__init__(path)

    def test_construct(self):
        """Test object type."""
        assert isinstance(self.test_secrets, Secrets)

    def test_properties(self):
        """Test property decorators."""
        assert self.test_secrets.values == {
            "pg_host": "cred1",
            "pg_port": "cred2",
            "pg_username": "cred3",
            "pg_password": "cred4",
            "pg_dbname": "cred5"
        }
