# -*- coding: utf-8 -*-
"""
Created on Sun Oct 22 21:09:52 2023

@author: Maximilian Hauser
"""

# import section ------------------------------------------------------------ #
from setuptools import setup

# readme -------------------------------------------------------------------- #
with open("README.md", "r") as fh:
    long_description = fh.read()

# setup --------------------------------------------------------------------- #
setup(name="hexlogic", 
      version="0.0.3", 
      description="HexLogic aims to be a Python package, without dependencies outside of the built-in library, providing fully-documented functions to deal with the relations between objects on a hexagon tiled grid. Including conversion from „hexagonal“ to „pixel“ coordinates and pathfinding with varying movement cost. As well as various operations like line-drawing.",
      py_modules=["hexlogic"],
      package_dir={"": "src"},
      classifiers=[
    "Programming Language :: Python :: 3",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent"
    ],
      long_description=long_description,
      long_description_content_type="markdown",
      url="https://github.com/MaximilianHauser/HexLogic",
      author="Maximilian Hauser",
      author_email="maxi.hauser@protonmail.com"
      )
