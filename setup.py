from setuptools import setup, find_namespace_packages

# read the contents of the README file
from os import path

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="target_matcher",
    version="0.0.1",
    description="A wrapper class for extended rule-based matching in spaCy.",
    author="medSpaCy",
    author_email="medspacy.dev@gmail.com",
    packages=["target_matcher"],
    install_requires=["spacy>=2.2.2"],
    long_description=long_description,
    long_description_content_type="text/markdown"
)