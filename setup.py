"""A setuptools based setup module."""
from os import path
from setuptools import setup, find_packages
from io import open

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="jiggy",
    version="0.0.1",
    description="Workflow management engine",
    long_description=long_description,
    url="https://github.com/thejig/jiggy",
    author="Mitchell Bregman, Leon Kozlowski",
    author_email="mitchbregs@gmail.com, leonkozlowski@gmail.com",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
    keywords="workflow management engine",
    packages=find_packages(),
    install_requires=[
        "python-dotenv",
        "pytest",
        "mock",
        "pyyaml"
    ],
)