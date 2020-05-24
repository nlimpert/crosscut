import os
import sys

# General configuration of Sphinx and extensions
needs_sphinx = '1.6.7'
needs_extensions = {
    'sphinx.ext.ifconfig': '1.0',
    'sphinx.ext.mathjax': '1.0',
    'sphinx.ext.todo': '1.0'
}
sys.path.append(os.path.abspath('%s%s_extension' % (os.curdir, os.sep)))
extensions = [
    'sphinx.ext.ifconfig',
    'sphinx.ext.mathjax',
    'sphinx.ext.todo',
    'rosin.didactic',
    'rosin.gui',
    'rosin.meta',
    'rosin.ros_element'
]
master_doc = 'index'
templates_path = ['_template']
exclude_patterns = []
pygments_style = 'sphinx'
language = 'en'

# General project information
project = "ROS-I Academy"
project_base = project.replace(' ', '_')
copyright = "2019, MASCOR Institute, FH Aachen"
description = ''
author = [
    "Nicolas Limpert",
    "Marcus Meeßen",
    "Patrick Wiesen"
]
version = "1.0"
release = "1.0-r1"

# Options for HTML
html_theme = 'sphinx_rtd_theme'
html_theme_options = {}
html_show_sphinx = False
html_show_sourcelink = False
html_static_path = ['_static']
html_extra_path = ['_extra']

# Options for LaTeX
latex_engine = 'pdflatex'
latex_documents = [
    (master_doc, '%s.tex' % project_base, project,
     ' \\and '.join(author), 'manual')
]
latex_elements = {
    'papersize': 'a4paper',
    'pointsize': '10pt',
    'preamble': r'''
    \makeatletter
      \usepackage{fancyhdr}
      \pagestyle{normal}
      \fancypagestyle{normal}{
        \fancyhf{}
        \fancyhead[L,LO,LE]{%
          MASCOR Institute \newline%
          FH Aachen UoAS \newline%
        }
        \fancyhead[C,CO,CE]{%
          \centering%
          \textbf{\@title}%
        }
        \fancyhead[R,RO,RE]{%
          \raggedleft%
          \nouppercase{\leftmark} \linebreak%
          \nouppercase{\rightmark} \linebreak%
        }
        \renewcommand{\headrulewidth}{0.4pt}
        \fancyfoot[L,LO,LE]{%
          \raisebox{0pt}{%
            \smash{%
              \hspace{-0.625cm}%
              \includegraphics[height=1.8cm]{../../_resource/image/logo/fh_aachen_left_black.pdf}%
            }%
          }%
          ~\includegraphics[height=0.6cm]{../../_resource/image/logo/mascor_left_no_fh_aachen.pdf}%
          \quad\includegraphics[height=0.6cm]{../../_resource/image/icon/cc-by-nc-nd-eu.pdf}%
        }
        \fancyfoot[C,CO,CE]{%
          \centering%
          \py@HeaderFamily\thepage%
        }
        \fancyfoot[R,RO,RE]{%
          \includegraphics[height=.6cm]{../../_resource/image/logo/european_union.pdf}%
          ~\parbox[b][.6cm][c]{2cm}{%
            \fontsize{3mm}{1.5mm}\selectfont\sf H2020~funded\\ GA\,no.\,732287%
          }%
          \quad\raisebox{0.75mm}{%
            \smash{%
              \includegraphics[height=1cm]{../../_resource/image/logo/rosin.pdf}%
              \hspace*{-1.1cm}%
            }%
          }%
        }
        \renewcommand{\footrulewidth}{0.4pt}
      }
      \fancypagestyle{plain}{
        \fancyhf{}
        \pagestyle{normal}
      }
      \fancypagestyle{empty}{
        \fancyhf{}
        \fancyhead[L,LO,LE,C,CO,CE,R,RO,RE]{}
        \fancyfoot[L,LO,LE,C,CO,CE,R,RO,RE]{}
        \renewcommand{\headrulewidth}{0pt}
        \renewcommand{\footrulewidth}{0pt}
      }
    \makeatother
    \renewcommand{\chaptermark}[1]{\markboth{#1}{}}
    \renewcommand{\sectionmark}[1]{\markright{#1}{}}
    ''',
    'figure_align': 'htbp',
}

# Options for HTML Help
htmlhelp_basename = project_base

# Options for manual page
man_pages = [
    (master_doc, project_base.lower(), project, author, 1)
]

# Options for Texinfo
texinfo_documents = [
    (master_doc, project_base, project, '@*'.join(author),
     project_base, description, 'Miscellaneous')
]

# Numbering and referencing of figures, tables, listings, and sections
numfig = True
numfig_format = {
    'figure': 'Figure %s',
    'table': 'Table %s',
    'code-block': 'Listing %s',
    'section': 'Section %s'
}

# Automatic conversion of quotes, dashes, and ellipses
smartquotes = True
smartquotes_action = 'qDe'

# If true, `todo` and `todoList` produce output, else they produce nothing.
todo_include_todos = True

# Tags for topic and selectors that always apply
tags.add('guideline')
tags.add('guideline_level_all')
tags.add('guideline_scenario_all')
tags.add('glossary_general')
tags.add('contributors')

# Miscellaneous settings
raw_enabled = True
show_authors = True
keep_warnings = True  # used for debugging