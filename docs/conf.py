"""Sphinx configuration."""
project = "python-spielplatz"
copyright = "2023, Travis Thompson"
author = "Travis Thompson"

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx_click",
    "myst_parser",
]
autodoc_typehints = "description"
html_theme = "furo"
