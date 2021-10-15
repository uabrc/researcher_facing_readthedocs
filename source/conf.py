from pathlib import Path, PurePath
from typing import List, Union

PathLike = Union[Path, PurePath, str]


def build_inline_code_highlighting_roles() -> str:
    FOLDER = PurePath("../res/")
    with open(file=FOLDER / "inline_languages.txt", mode="r") as f:
        lexers = f.readlines()

    roles: List[str] = []
    for lexer in lexers:
        lexer = lexer.strip().lower()
        role_parts: List[str] = [
            f".. role:: {lexer}(code)",
            f":language: {lexer}",
            ":class: highlight",
        ]
        role: str = "\n   ".join(role_parts)
        roles.append(role)

    out: str = "\n\n".join(roles)
    # with open(file=FOLDER / "inline_lanugage_roles.txt", mode="w") as f:
    #     f.write(out)

    return out


# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html


# ! Please use the Black formatter to format this document before pushing.


# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
# import os
# import sys
# sys.path.insert(0, os.path.abspath('.'))


# -- Project information -----------------------------------------------------

# TODO change these lines
project = "UAB RC Documentation"
copyright = "2021, William Warriner"
author = "William Warriner"


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = ["sphinx.ext.autosectionlabel", "sphinxcontrib.bibtex"]
bibtex_bibfiles = ["_test/bibtex/mybib.bib"]

# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = []


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = "sphinx_rtd_theme"

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ["_static"]
html_logo = "html/_static/uab-it-logo.png"
html_theme_options = {
    "logo_only": True,
    "display_version": False,
    # toc options
    "collapse_navigation": True,
    "sticky_navigation": True,
    "navigation_depth": 4,
    "includehidden": True,
    "titles_only": False,
}

# Prolog:
rst_prolog = f"""
{build_inline_code_highlighting_roles()}
"""
