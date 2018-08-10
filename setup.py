
import os.path
from setuptools import setup

# Get the long description from the README file
here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'README.md')) as fp:
    long_description = fp.read()


setup(
    author="@LoisaidaSam",
    author_email="sam.sandberg@gmail.com",
    description="A custom CSV reader implementation with direct file access",
    long_description=long_description,
    long_description_content_type='text/markdown',
    keywords=["csv"],
    license="MIT",
    name="csv-position-reader",
    packages=["csv_position_reader"],
    test_suite="tests",
    url="https://github.com/loisaidasam/csv-position-reader",
    version="0.1.0",
)
