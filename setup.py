import os

try:
    from setuptools import setup
except ImportError:
    exit("This package requires Python version >= 3.6 and Python's setuptools")

here = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(here, 'requirements.txt')) as f:
    requirements = f.read().splitlines()

with open(os.path.join(here, 'options_freedom', 'VERSION')) as f:
    lines = f.read().splitlines()
    try:
        version = [line.split('=')[1] for line in lines if line.startswith('V')][0]
    except IndexError:
        exit("Invalid package version in %s" % os.path.join(here, 'options_freedom', 'VERSION'))

setup(
    name="options-freedom",
    version=version,
    description="Options analyzer.",
    long_description="Options analyzer.",
    url="https://github.com/viclule/options_analyzer",
    author='Vicente Guerrero',
    author_email='vic.lule@googlemail.com',
    packages=["options_freedom", "options_freedom.symbol", "options_freedom.conditions",
    "options_freedom.conditions.close", "options_freedom.conditions.open", "options_freedom.data",
    "options_freedom.data.options", "options_freedom.data.quotes", "options_freedom.data.options.spy", "options_freedom.data.quotes.vix",
    "options_freedom.models", "options_freedom.option", "options_freedom.pattern",
    "options_freedom.simulator", "options_freedom.strategy"],
    include_package_data=True,
    install_requires=requirements,
)
