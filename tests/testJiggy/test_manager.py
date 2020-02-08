"""Test Manager Classes."""
import pytest

from unittest import TestCase

from src.jiggy.manager import Manager


class TestManager(TestCase):
    """Test suite for src.jiggy.manager."""

    def __init__(self, path):
        """Construct TestCase."""
        self.test_manager = Manager(
            location="testData/minimal_test_case.yml"
        )
        super(TestManager, self).__init__(path)

    def test_construct(self):
        """Test object type."""
        assert isinstance(self.test_manager, Manager)

    def test_properties(self):
        """Test property decorators."""
        assert self.test_manager.name == "Gets todays date, then finds weekday"
        assert self.test_manager.author == "xyz@company.com"
        assert self.test_manager.version == "0.0.1"
        assert self.test_manager.description == (
            "Creates a database, gets a date, pushes to database"
        )
        assert isinstance(self.test_manager.pipeline, dict)
        assert self.test_manager.secrets == {
            "location": ".env",
            "source": "jiggy.EnvSecrets"
        }
        assert self.test_manager.executor == "sequential"
        assert isinstance(self.test_manager.associate, tuple)