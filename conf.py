import os
import sys

from sphinx.util.tags import Tags

# General configuration of Sphinx and extensions
needs_sphinx = '1.8.4'
needs_extensions = {
    'sphinx.ext.ifconfig': '1.0',
    'sphinx.ext.mathjax': '1.0',
    'sphinx.ext.todo': '1.0',
}
sys.path.append(os.path.abspath(os.path.join(os.curdir, '_extension')))
extensions = [
    'sphinx.ext.ifconfig',
    'sphinx.ext.mathjax',
    'sphinx.ext.todo',
    'sphinxcontrib.rsvgconverter',
    'rosin.didactic',
    'rosin.gui',
    'rosin.meta',
    'rosin.ros_element',
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
author = "Nicolas Limpert \\and Marcus Meeßen \\and Patrick Wiesen"
version = "1.0"
release = "1.0-r1"

# Options for HTML
html_theme = 'sphinx_rtd_theme'
html_theme_options = {}
html_show_sphinx = False
html_show_sourcelink = False
html_copy_source = False
html_static_path = ['_static']
html_extra_path = ['_extra']

# Options for LaTeX
latex_engine = 'pdflatex'
latex_documents = [
    (master_doc, '%s.tex' % project_base, project, author, 'manual'),
]
latex_elements = {
    'papersize': 'a4paper',
    'pointsize': '10pt',
    'preamble': r'''
    \usepackage{fancyhdr}
    \setlength{\headheight}{36pt}
    \makeatletter
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
          \quad\includegraphics[height=0.6cm]{../../_resource/image/icon/cc_by-nc-nd_eu.pdf}%
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
def hex_hash(data: str) -> str:
    from hashlib import md5
    return 'H%s' % md5(data.encode('utf-8')).hexdigest()


global tags
tags.add(hex_hash('guideline'))
tags.add('%s_level_all' % hex_hash('guideline'))
tags.add('%s_scenario_all' % hex_hash('guideline'))
tags.add(hex_hash('general_glossary'))
tags.add(hex_hash('contributors'))

# Miscellaneous settings
raw_enabled = True
show_authors = True
keep_warnings = True  # used for debugging

# Options for rosin.Didactic
didactic_levels = {
    'beginner': "Beginner",
    'intermediate': "Intermediate",
    'advanced': "Advanced",
}
didactic_scenarios = {
    # operating systems
    'linux': "Linux",
    'windows': "Windows",
    'mac_os': "MacOS",
    # programming languages
    'cpp': "C++",
    'python': "Python",
    # robot platforms
    'kuka_you_bot': "KUKA YouBot",
    'turtle_bot_3': "TurtleBot3",
    'turtle_sim': "TurtleSim",
    'universal_robots_ur': "Universal Robots UR Series",
    'universal_robots_ur3': "Universal Robots UR3",
    'universal_robots_ur5': "Universal Robots UR5",
    'yaskawa_sia10f': "YASKAWA SIA10F",
}
