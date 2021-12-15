# -*- coding: utf-8 -*-
#
# Configuration file for the Sphinx documentation builder.
#
# This file does only contain a selection of the most common options. For a
# full list see the documentation:
# http://www.sphinx-doc.org/en/master/config

import os


project = 'fd.partialdate'
copyright = '2018, 2021, Fred L. Drake, Jr.'
author = 'Fred Drake'

# The full version, including alpha/beta/rc tags
release = os.environ.get('VERSION') or ''
version = release or '(development)'

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.autodoc.typehints',
    'sphinx.ext.intersphinx',
]

intersphinx_mapping = {
    'python': ('https://docs.python.org/3', None),
}

source_suffix = '.rst'
master_doc = 'index'

html_theme = 'sphinx_rtd_theme'

html_theme_options = {
    # 'issues_url': ('https://github.com/'
    #                'freddrake/fd.partialdate/issues/'),
}

html_last_updated_fmt = ''

# Grouping the document tree into LaTeX files. List of tuples
# (source start file, target name, title,
#  author, documentclass [howto, manual, or own class]).
latex_documents = [
    (master_doc, 'fd-partialdate.tex', 'fd.partialdate Documentation',
     'Fred Drake', 'manual'),
]

autodoc_default_options = {
    'members': True,
}

autoclass_content = 'class'
autodoc_class_signature = 'separated'
autodoc_member_order = 'bysource'
autodoc_typehints = 'description'

# Bibliographic Dublin Core info.
epub_title = 'fd.partialdate'

# A list of files that should not be packed into the epub file.
epub_exclude_files = ['search.html']
