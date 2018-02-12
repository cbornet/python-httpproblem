import subprocess
from setuptools import setup

# Try to create an rst long_description from README.md
try:
    args = 'pandoc', '--to', 'rst', 'README.md'
    long_description = subprocess.check_output(args).decode('utf-8')
except Exception as error:
    print('README.md conversion to reStructuredText failed. Error:')
    print(error)
    print('Setting long_description to None.')
    long_description = None

setup(
    name='httpproblem',
    version='0.2.0',
    url='https://github.com/cbornet/python-httpproblem',
    download_url='https://pypi.python.org/pypi/httpproblem',
    license='MIT',
    author='Christophe Bornet',
    author_email='cbornet@hotmail.com',
    description='Utility library to work with RFC7807 Problem Details for HTTP APIs',
    long_description=long_description,
    packages=['httpproblem'],
    keywords='rfc7807 problem http json',
    platforms=['any']
)
