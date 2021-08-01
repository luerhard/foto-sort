from setuptools import setup

setup(
    name="fotosort",
    version="0.2.0",
    py_modules="fotosort",
    install_requires=["click", "pyexiftool", "reverse-geocode", "pillow"],
    entry_points={"console_scripts": ["fotoingest = fotosort.main:main"]},
)
