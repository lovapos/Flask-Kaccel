import os
import sys
sys.path.insert(0, os.path.abspath('../'))

# -- General configuration ------------------------------------------------

extensions = ['sphinx.ext.autodoc', 'sphinx.ext.doctest', 'sphinx.ext.coverage', 'sphinx.ext.viewcode']
templates_path = ['_templates']
source_suffix = '.txt'
master_doc = 'index'
project = 'Flask-Kaccel'
copyright = '2017, Bapakode Open Source'
author = 'Bapakode Open Source'
version = '1.0'
release = '1.0'
language = None
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']
pygments_style = 'sphinx'
todo_include_todos = False
autoclass_content = 'both'
autodoc_member_order = 'bysource'

# -- Options for HTML output ----------------------------------------------

html_theme = 'flask'
html_theme_options = {
    "github_fork": "bapakode/Flask-Kaccel",
    "index_logo": "logo.png",
    "index_logo_height": "150px",
}
html_static_path = ['_static']


# -- Options for HTMLHelp output ------------------------------------------

htmlhelp_basename = 'Flask-Kacceldoc'


# -- Options for LaTeX output ---------------------------------------------

latex_elements = {
    # The paper size ('letterpaper' or 'a4paper').
    #
    # 'papersize': 'letterpaper',

    # The font size ('10pt', '11pt' or '12pt').
    #
    # 'pointsize': '10pt',

    # Additional stuff for the LaTeX preamble.
    #
    # 'preamble': '',

    # Latex figure (float) alignment
    #
    # 'figure_align': 'htbp',
}

latex_documents = [(master_doc, 'Flask-Kaccel.tex', 'Flask-Kaccel Documentation','Bapakode Open Source', 'manual'),]

# -- Options for manual page output ---------------------------------------

man_pages = [(master_doc, 'flask-kaccel', 'Flask-Kaccel Documentation', [author], 1)]

# -- Options for Texinfo output -------------------------------------------
texinfo_documents = [(master_doc, 'Flask-Kaccel', 'Flask-Kaccel Documentation',author, 'Flask-Kaccel', 'One line description of project.','Miscellaneous'),]