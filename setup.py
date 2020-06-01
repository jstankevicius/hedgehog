from setuptools import setup
import os
import sys

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name="hedgehog",
    version="0.0.0",
    description="An algorithmic trader.",
    author="Justas Stankevicius",
    author_email="jstankevicius@protonmail.com",
    packages=["hedgehog", "tests", "scripts"],
    long_description=read("README.md"),
    classifiers=[
        "Development Status :: 1", # "Planning" status
    ],
)