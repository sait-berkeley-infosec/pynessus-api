from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'DESCRIPTION.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='pynessus-api',
    version='1.0dev',
    description='A Python interface to the Nessus API',
    long_description=long_description,
    url='https://github.com/sait-berkeley-infosec',
    author='Arlan Jaska',
    license='MIT',
    packages=find_packages(),
    install_requires=[
    "xmltodict >= 0.9.0",
    ],
) 
