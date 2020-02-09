"""Test Manager Classes."""
from unittest import TestCase

from src.jiggy.pipeline import Pipeline


class TestPipeline(TestCase):
    """Test suite for src.jiggy.manager."""

    def __init__(self, path):
        """Construct TestCase."""
        self.test_pipeline = Pipeline(
            location="testData/minimal_test_case.yml"
        )
        super(TestPipeline, self).__init__(path)

    def test_construct(self):
        """Test object type."""
        assert isinstance(self.test_pipeline, Pipeline)

    def test_properties(self):
        """Test property decorators."""
        assert self.test_pipeline.name == "Gets todays date, then finds weekday"
        assert self.test_pipeline.author == "xyz@company.com"
        assert self.test_pipeline.version == "0.0.1"
        assert self.test_pipeline.description == (
            "Creates a database, gets a date, pushes to database"
        )
        assert isinstance(self.test_pipeline.pipeline, dict)
        assert self.test_pipeline.secrets == {
            "location": ".env",
            "source": "jiggy.EnvSecrets"
        }
        assert isinstance(self.test_pipeline.tasks, list)
        assert self.test_pipeline.executor == "sequential"
