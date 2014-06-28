from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

tests_require = [
    'mock >= 1.0.1',
]

install_requires = [
    'xmltodict >= 0.9.0',
]

setup(
    name='pynessus-api',
    version='1.0dev',
    description='A Python interface to the Nessus API',
    long_description=long_description,
    url='https://github.com/sait-berkeley-infosec/pynessus-api',
    author='Arlan Jaska',
    author_email='ajaska@berkeley.edu',
    license='MIT',
    packages=find_packages(),
    install_requires=install_requires,
    tests_require=tests_require,
) 
