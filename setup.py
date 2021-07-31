
from setuptools import setup

setup(
    name="fotosort",
    version="0.1.0",
    py_modules="fotosort",
    install_requires=["click", "pyexiftool", "reverse-geocode"],
    entry_points="""
    [console_scripts]
    fotoingest=fotosort
    """
)