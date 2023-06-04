from setuptools import setup, find_packages


with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='pgo_storage_cleanup_calcyiv',
    version='0.1.0',
    description='Takes the exported history from calcyiv, and determines the best PVP and overall IV of each pokemon, allowing for easy cleaning and organizing of pokemon storage in Pokemon Go.',
    long_description=readme,
    author='Erik Liubakka',
    url='https://github.com/eliubakk/pgo_storage_cleanup_calcyiv',
    license=license,
    packages=find_packages(exclude=('tests', 'docs'))
)