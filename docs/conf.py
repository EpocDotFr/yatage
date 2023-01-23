# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'YATAGE'
copyright = '2023, <a href="https://epoc.fr/">Epoc</a>'
author = '<a href="https://epoc.fr/">Epoc</a>'
release = '1.0.0b1'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'sphinx.ext.intersphinx',
    'sphinx.ext.autosectionlabel',
    'sphinx.ext.todo',
]

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

todo_include_todos = True

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'alabaster'

html_theme_options = {
    'show_powered_by': False,
    'github_button': False,
    'github_banner': True,
    'github_user': 'EpocDotFr',
    'github_repo': 'yatage',
    'fixed_sidebar': True,
    'logo_name': True,
    'description': 'Yet Another Text Adventure Game Engine',
    'logo': 'logo_transparent.png',
    'logo_text_align': 'center',
    'extra_nav_links': {
        'PyPI': 'https://pypi.org/project/yatage/',
        'Source Code': 'https://github.com/EpocDotFr/yatage',
        'Issue Tracker': 'https://github.com/EpocDotFr/yatage/issues',
        'Roadmap': 'https://github.com/EpocDotFr/yatage/milestones',
        'Changelog': 'https://github.com/EpocDotFr/yatage/releases',
    }
}

html_static_path = ['_static']

html_sidebars = {'**': ['about.html', 'navigation.html', 'searchbox.html']}

html_show_sourcelink = False
html_show_sphinx = False
html_show_copyright = True
html_favicon = 'favicon.ico'

intersphinx_mapping = {
    'python': ('https://docs.python.org/3.8', None),
}
