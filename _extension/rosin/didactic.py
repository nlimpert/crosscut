# Copyright (C) 2019-2020 MASCOR Institute. All rights reserved.

"""
The rosin.Didactic extension of Sphinx provides several text roles and
directives that are missing in the vanilla version but required or at least
useful for teaching ROS-I.

Example:
```
While this text is shown normal, :strike:`this text will be crossed out`.

.. task:: An admonition for highlighting tasks.

.. role:author:: A note that is only visible in the author's edition.

.. role:teacher:: A note that is only visible in the teacher's edition.

.. role:tutor:: A note that is only visible in the tutor's edition.

.. role:mixed:: { author | teacher | tutor }

   A note that is visible for several roles.

.. level:: { beginner | intermediate | advanced | ... }

   This text is only visible if one of the above levels or "all" is included in
   the configured tags. For example, "<filename>_level_intermediate" or
   "<filename>_level_all" have to be added to the "tags" object. Define allowed
   keywords with the `didactic_levels` option.

.. scenario:: { turtle_bot_3 | python | ... }

   This text is only visible if one of the above scenarios or "all" is included
   in the configured tags. For example, "<filename>_scenario_turtle_bot_3" or
   "<filename>_scenario_all" have to be added to the "tags" object. Define
   allowed keywords with the `didactic_scenarios` option.
```
"""

__author__ = "Meeßen, Marcus"
__copyright__ = "Copyright (C) 2019-2020 MASCOR Institute"
__version__ = "1.5"

import re
from typing import Dict, List, Set, Tuple, Type

from docutils.nodes import Admonition, Element, General, Inline, Node, \
    TextElement, inline, title
from docutils.parsers.rst import Directive, directives
from docutils.parsers.rst.directives.admonitions import BaseAdmonition
from sphinx.application import Sphinx
from sphinx.config import Config
from sphinx.directives import Only
from sphinx.domains import Domain
from sphinx.errors import ExtensionError
from sphinx.writers.html import HTMLTranslator
from sphinx.writers.latex import LaTeXTranslator


# noinspection PyPep8Naming
class strike(Inline, TextElement):
    pass


def visit_strike_html(self: HTMLTranslator, _node) -> None:
    self.body.append('<s>')


def depart_strike_html(self: HTMLTranslator, _node) -> None:
    self.body.append('</s>')


def visit_strike_latex(self: LaTeXTranslator, _node) -> None:
    self.body.append('\\s''out{')


def depart_strike_latex(self: LaTeXTranslator, _node) -> None:
    self.body.append('}')


# noinspection PyPep8Naming
class task(Admonition, Element):
    pass


def visit_task_html(self: HTMLTranslator, node: task) -> None:
    self.body.append('<div class="admonition task warning">')
    node.insert(0, title('task', 'Task'))
    self.set_first_last(node)


def depart_task_html(self: HTMLTranslator, _node) -> None:
    self.body.append('</div>')


def visit_task_latex(self: LaTeXTranslator, _node) -> None:
    self.body.append('\n\\begin{sphinx''admonition}{note}{Task:}')


def depart_task_latex(self: LaTeXTranslator, _node) -> None:
    self.body.append('\\end{sphinx''admonition}\n')


class Task(BaseAdmonition):
    node_class = task


def visit_role_html(node_class: Type, heading: str):
    def func(self: HTMLTranslator, node: node_class) -> None:
        self.body.append('<div class="admonition note %s">'
                         % node_class.__name__)
        node.insert(0, title('%s-note' % node_class.__name__,
                             '%s' % heading))
        self.set_first_last(node)

    return func


def depart_role_html():
    def func(self: HTMLTranslator, _node) -> None:
        self.body.append('</div>')

    return func


def visit_role_latex(heading: str):
    def func(self: LaTeXTranslator, _node) -> None:
        self.body.append('\n\\begin{sphinx''admonition}{note}{%s:}' % heading)

    return func


def depart_role_latex():
    def func(self: LaTeXTranslator, _node) -> None:
        self.body.append('\\end{sphinx''admonition}\n')

    return func


class RoleAdmonition(BaseAdmonition):
    enabled: bool = False

    def run(self) -> List[Node]:
        return super().run() if self.enabled is True else []


# noinspection PyPep8Naming
class role_author(Admonition, Element):
    pass


class Author(RoleAdmonition):
    node_class = role_author


# noinspection PyPep8Naming
class role_teacher(Admonition, Element):
    pass


class Teacher(RoleAdmonition):
    node_class = role_teacher


# noinspection PyPep8Naming
class role_tutor(Admonition, Element):
    pass


class Tutor(RoleAdmonition):
    node_class = role_tutor


# noinspection PyPep8Naming
class role_mixed(Admonition, Element):
    pass


class Mixed(Directive):
    has_content = True
    required_arguments = 1
    final_argument_whitespace = True

    def run(self) -> List[Node]:
        active_roles = self.arguments[0].split()
        raw_text = ' '.join(self.content)
        inline_text = inline(text=raw_text)
        admonitions = []

        for role in [Author, Teacher, Tutor]:
            if role.enabled and role.__name__.lower() in active_roles:
                admonitions.append(role.node_class(raw_text, inline_text))

        return admonitions


class RoleDomain(Domain):
    name: str = 'role'
    label: str = "Intended Role of a User"
    directives: Dict[str, Type[Directive]] = {
        'mixed': Mixed,
        'author': Author,
        'teacher': Teacher,
        'tutor': Tutor,
    }

    # noinspection SpellCheckingInspection
    def merge_domaindata(self, *args, **kwargs) -> None:
        pass

    # noinspection SpellCheckingInspection
    def resolve_any_xref(self, *args, **kwargs) -> List[Tuple[str, Node]]:
        pass


# noinspection PyPep8Naming
class level(General, Element):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.levels: Set[str] = set()


def visit_level_html(self: HTMLTranslator, node: level) -> None:
    self.body.append(
        '<div class="level"><div><div class="level-badges">%s</div><div>'
        % ''.join(['<span class="level-label">%s</span>'
                   % Level.levels[label]
                   for label in node.levels])
    )
    self.set_first_last(node)


def depart_level_html(self: HTMLTranslator, _node) -> None:
    self.body.append('</div></div><div class="level-bar"></div></div>')


def visit_level_latex(self: LaTeXTranslator, node: level) -> None:
    self.body.append('\\begin{left''bar}{\\sl\\tiny %s\\par}'
                     % ', '.join(['%s' % Level.levels[label]
                                  for label in node.attributes['levels']]))


def depart_level_latex(self: LaTeXTranslator, _node) -> None:
    self.body.append('\\end{left''bar}')


class Level(Only):
    option_spec = {'raw': directives.class_option}
    levels: Dict[str, str]

    def run(self) -> List[Node]:
        only = super().run()[0]
        node = level()
        node.levels = list(option.replace("-", "_")
                           for option in self.options['raw'])
        only.children, node.children = node, only.children
        return [only]


# noinspection PyPep8Naming
class scenario(General, Element):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.scenarios: Set[str] = set()


def visit_scenario_html(self: HTMLTranslator, node: scenario) -> None:
    self.body.append(
        '<div class="scenario"><div><div class="scenario-badges">%s</div><div>'
        % ''.join(['<span class="scenario-label">%s</span>'
                   % Scenario.scenarios[label]
                   for label in node.scenarios])
    )
    self.set_first_last(node)


def depart_scenario_html(self: HTMLTranslator, _node) -> None:
    self.body.append('</div></div><div class="scenario-bar"></div></div>')


def visit_scenario_latex(self: LaTeXTranslator, node: scenario) -> None:
    self.body.append('\\begin{left''bar}{\\sl\\tiny %s\\par}'
                     % ', '.join(['%s' % Scenario.scenarios[label]
                                  for label in node.attributes['scenarios']]))


def depart_scenario_latex(self: LaTeXTranslator, _node) -> None:
    self.body.append('\\end{left''bar}')


class Scenario(Only):
    option_spec = {'raw': directives.class_option}
    scenarios: Dict[str, str]

    def run(self) -> List[Node]:
        only = super().run()[0]
        node = scenario()
        node.scenarios = list(option.replace("-", "_")
                              for option in self.options['raw'])
        only.children, node.children = node, only.children
        return [only]


def generate_expression(app: Sphinx, doc_name: str, directive: str,
                        original: str) -> str:
    invalid_keywords = re.search(r'(all|not|and|or|is|True|False|None)',
                                 original)
    if invalid_keywords is not None:
        raise ExtensionError("Invalid keyword '%s' in %s expression."
                             % (invalid_keywords.group(1), directive))

    selectors: List[str] = original.split()

    valid_keywords: List[str] = {
        'level': list(Level.levels.keys()),
        'scenario': list(Scenario.scenarios.keys()),
    }[directive]

    if not all(selector in valid_keywords for selector in selectors):
        raise ExtensionError("Invalid expression '%s' in %s directive, "
                             "allowed specifiers are %s."
                             % (original, directive, valid_keywords))

    selectors += ['all']

    for index, selector in enumerate(selectors):
        selectors[index] = ('%s_%s_%s or %s_%s_%s' %
                            (app.config.hex_hash(doc_name), directive, selector,
                             app.config.hex_hash('all'), directive, selector))

    return ' or '.join(selectors)


def process_selectors(app: Sphinx, doc_name, source: List[str]) -> None:
    if not len(source) > 0:
        raise ExtensionError("Could not process an empty source list.")

    line_groups: List[str] = re.split(r'(\n{2,})', source[0])

    for index, line_group in enumerate(line_groups):
        line_groups[index] = re.sub(
            r'^(([ ]*)\.\. (level|scenario):: )([\n\w\- ]+)',
            lambda x: '%s%s\n%s   :raw: %s' % (x.group(1),
                                               generate_expression(app,
                                                                   doc_name,
                                                                   x.group(3),
                                                                   x.group(4)),
                                               x.group(2),
                                               re.sub(r'\n', ' ', x.group(4))),
            line_group)

    source[0] = str().join(line_groups)


def config_inited(_app, config: Config) -> None:
    Level.levels = config['didactic_levels']
    Scenario.scenarios = config['didactic_scenarios']


def setup(app: Sphinx) -> None:
    if 'hex_hash' not in app.config:
        app.add_config_value('hex_hash', None, 'env')
    app.add_config_value('didactic_levels', {}, 'env')
    app.add_config_value('didactic_scenarios', {}, 'env')

    if 'author' in app.tags:
        Author.enabled = True
    if 'teacher' in app.tags:
        Teacher.enabled = True
    if 'tutor' in app.tags:
        Tutor.enabled = True

    app.add_stylesheet('style/didactic.css')
    app.add_latex_package('ul''em')
    app.add_domain(RoleDomain)
    app.add_node(strike,
                 html=(visit_strike_html, depart_strike_html),
                 latex=(visit_strike_latex, depart_strike_latex),
                 )
    app.add_node(task,
                 html=(visit_task_html, depart_task_html),
                 latex=(visit_task_latex, depart_task_latex),
                 )
    app.add_node(role_tutor,
                 html=(visit_role_html(role_tutor, "Tutor Note"),
                       depart_role_html()),
                 latex=(visit_role_latex("Tutor Note"), depart_role_latex()),
                 )
    app.add_node(role_author,
                 html=(visit_role_html(role_author, "Author Note"),
                       depart_role_html()),
                 latex=(visit_role_latex("Author Note"), depart_role_latex()),
                 )
    app.add_node(role_teacher,
                 html=(visit_role_html(role_teacher, "Teacher Note"),
                       depart_role_html()),
                 latex=(visit_role_latex("Teacher Note"), depart_role_latex()),
                 )
    app.add_node(role_mixed)
    app.add_node(level,
                 html=(visit_level_html, depart_level_html),
                 latex=(visit_level_latex, depart_level_latex),
                 )
    app.add_node(scenario,
                 html=(visit_scenario_html, depart_scenario_html),
                 latex=(visit_scenario_latex, depart_scenario_latex),
                 )
    app.add_generic_role('strike', strike)
    app.add_directive('task', Task)
    app.add_directive('level', Level)
    app.add_directive('scenario', Scenario)
    app.connect('source-read', process_selectors)
    app.connect('config-inited', config_inited)
