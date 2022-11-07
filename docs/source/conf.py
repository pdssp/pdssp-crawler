# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
import os
import sys

sys.path.insert(0, os.path.abspath('../..'))

# import sphinx_rtd_theme
# import sphinx_click

# Get GFINDER version string
version_file = open(os.path.join('../..', 'VERSION'))
version = version_file.read().strip()

# -- Project information -----------------------------------------------------

project = 'PDSSP Crawler'
copyright = ''
author = 'Nicolas Manaud'
date = 'Oct 3, 2022'
# The full version, including alpha/beta/rc tags
release = version

rst_epilog = """
.. |version| replace:: v{}

.. |date| replace:: {}
""".format(version, date)

# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    'sphinx.ext.napoleon',
    'sphinx_click',
    'sphinx.ext.viewcode',
    'sphinx.ext.intersphinx',
    'sphinxcontrib.programoutput',
    'myst_nb',
    'sphinxcontrib.autodoc_pydantic'
    ]

# # autodoc-pydantic settings
# # https://autodoc-pydantic.readthedocs.io/en/stable/users/installation.html
# autodoc_pydantic_model_show_json = True
# autodoc_pydantic_settings_show_json = False

# myst_nb parameters
nb_execution_excludepatterns = ['build/jupyter_execute']
nb_execution_mode = "auto"
# https://myst-nb.readthedocs.io/en/latest/computation/execute.html?highlight=nb_execution_mode#notebook-execution-modes

#pdf_documents = [('index', u'rst2pdf', u'Sample rst2pdf doc', u'Your Name'),]

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = [
    '_build',
    '**.ipynb_checkpoints',
    'build/jupyter_execute',
    'Thumbs.db',
    '.DS_Store',
    '.jupyter_cache',
    'jupyter_execute',
    'excluded/*.*',
    'notebooks/tests',
    'notebooks/use_cases',
]

source_suffix = {
    '.rst': 'restructuredtext',
    '.ipynb': 'myst-nb',
    '.myst': 'myst-nb'
}

autoclass_content = 'both' # includes __init__ constructor methods documentation

# -- Mapping -----------------------------------------------------------------

intersphinx_mapping = {
    'python': ('https://docs.python.org/3/', None),
    'numpy': ('https://numpy.org/doc/stable/', None),
    'matplotlib': ('https://matplotlib.org/stable/', None),
    'spiceypy': ('https://spiceypy.readthedocs.io/en/stable/', None),
}

# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
#html_theme = 'sphinx_rtd_theme'
# html_theme = 'sphinx_material'
html_theme = 'sphinx_book_theme'
html_title = 'PDSSP Crawler'

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']

html_favicon = '../images/favicon.png'

html_theme_options = {
    "use_download_button": "false",
    "use_fullscreen_button": "false",
    "logo_only": "true",
    "repository_url": "https://github.com/nmanaud/pdssp-crawler",
}
highlight_language = 'none'

# # Material theme options (see theme.conf for more information)
# html_theme_options = {
#
#     # Set the name of the project to appear in the navigation.
#     'nav_title': 'PDSSP Crawler',
#
#     # Set you GA account ID to enable tracking
#     # 'google_analytics_account': 'UA-XXXXX',
#
#     # Specify a base_url used to generate sitemap.xml. If not
#     # specified, then no sitemap will be built.
#     # 'base_url': 'https://project.github.io/project',
#
#     # Set the color and the accent color
#     'color_primary': 'blue',
#     'color_accent': 'light-blue',
#
#     # Set the repo location to get a badge with stats
#     'repo_url': 'https://github.com/nmanaud/pdssp-crawler',
#     'repo_name': 'pdssp-crawler',
#
#     # Visible levels of the global TOC; -1 means unlimited
#     'globaltoc_depth': 3,
#     # If False, expand all TOC entries
#     'globaltoc_collapse': False,
#     # If True, show hidden TOC entries
#     'globaltoc_includehidden': False,
# }

# html_css_files = [ 'css/custom.css' ]
html_logo = '../images/pdssp_logo.png'