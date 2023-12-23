# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

import os
import sys
from typing import List
from importlib import import_module
from jinja2.filters import FILTERS
import torch

mammoth_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(mammoth_path)
os.chdir(mammoth_path)

from datetime import date

project = 'Mammoth'
author = 'Pietro Buzzega, Matteo Boschini, Lorenzo Bonicelli, Aniello Panariello, Davide Abati, Angelo Porrello, Simone Calderara'
copyright = f'{date.today().year}, {author}'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = ['sphinx.ext.autodoc',
              'sphinx.ext.intersphinx',
              'sphinx.ext.autosummary',
              'sphinx.ext.napoleon',
              'sphinx.ext.viewcode',
              'sphinx.ext.viewcode',
              'sphinx_tabs.tabs',
              'sphinx-prompt',
              'sphinx_toolbox',
              'sphinx.ext.autosectionlabel']

github_username = 'grupposimo'
github_repository = 'mammoth'

intersphinx_mapping = {
    'python': ('https://docs.python.org/3', None),
    'torch': ('https://pytorch.org/docs/master/', None),
    'torchvision': ('https://pytorch.org/docs/master/', None),
    'numpy': ('https://numpy.org/doc/stable/', None),
}

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

# The suffix(es) of source filenames.
# You can specify multiple suffix as a list of string:
#
# source_suffix = ['.rst', '.md']
source_suffix = '.rst'

# The master toctree document.
master_doc = 'index'

# The language for content autogenerated by Sphinx. Refer to documentation
# for a list of supported languages.
#
# This is also used if you do content translation via gettext catalogs.
# Usually you set "language" from the command line for these cases.
language = 'en'

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns: List[str] = []

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = 'friendly'

# https://www.sphinx-doc.org/en/master/usage/configuration.html#confval-nitpicky
# This generates a lot of warnings because of the broken internal links, which
# makes the docs build fail because of the "fail_on_warning: true" option in
# the .readthedocs.yml config file
# nitpicky = True

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

# html_theme = 'alabaster'
html_theme = "furo"
html_title = "Mammoth"
html_static_path = ['_static']
html_favicon = 'images/logo.png'

autosummary_generate = True
numpydoc_show_class_members = False

# Disable docstring inheritance
autodoc_inherit_docstrings = False

# Show type hints in the description
autodoc_typehints = "description"

# Add parameter types if the parameter is documented in the docstring
autodoc_typehints_description_target = "documented_params"


def get_attributes(item, obj, modulename):
    """Filters attributes to be used in autosummary.

    Fixes import errors when documenting inherited attributes with autosummary.

    """
    module = import_module(modulename)
    if hasattr(getattr(module, obj), item):
        return f"{item}"
    else:
        return ""


def drop_torch_items(items, obj, module):
    """Filters attributes to be used in autosummary.

    Fixes import errors when documenting inherited attributes with autosummary.

    """
    mod = import_module(module)
    import_obj = getattr(mod, obj)
    fn_to_keep = import_obj.__dict__.keys()
    for item in items:
        if item in fn_to_keep and item != "__init__":
            yield item


def has_items(items, obj, module):
    """Filters attributes to be used in autosummary.

    Fixes import errors when documenting inherited attributes with autosummary.

    """
    mod = import_module(module)
    import_obj = getattr(mod, obj)
    fn_to_keep = import_obj.__dict__.keys()
    its = [item for item in items if item in fn_to_keep and item != "__init__"]
    return len(its) > 0


FILTERS["has_items"] = has_items
FILTERS["drop_torch_items"] = drop_torch_items
FILTERS["get_attributes"] = get_attributes
