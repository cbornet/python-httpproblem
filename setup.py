from os import path
from setuptools import setup

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.rst')) as f:
    long_description = f.read()

setup(
    name='httpproblem',
    version='0.1.1',
    url='https://github.com/cbornet/python-httpproblem',
    license='MIT',
    author='Christophe Bornet',
    author_email='cbornet@hotmail.com',
    description='Utility library to work with RFC7807 Problem Details for HTTP APIs',
    long_description=long_description,
    packages=['httpproblem'],
    keywords='rfc7807 problem http json',
)
