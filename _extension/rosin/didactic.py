# Copyright (C) 2019 MASCOR Institute. All rights reserved.

"""
The rosin.Didactic extension of Sphinx provides several text roles and
directives that are missing in the vanilla version but required or at least
useful for teaching ROS-I. This extension requires rosin.Meta to work properly.

Example:
```
:strike:`this text will be stiked through`

.. task:: An admonition for highlighting tasks.

.. internal:: An internal note that should be visible for the instructor or
   author only.

.. level:: beginner intermediate advanced

   This text is only visible if one of the above levels or "all" is included in
   the configured tags. For example, "topic_level_beginner" or "topic_level_all"
   have to be added to the "tags" object.

.. scenario:: turtle_bot_3 python

   This text is only visible if one of the above scenarios or "all" is included
   in the configured tags. For example, "topic_scenario_turtle_bot_3" or
   "topic_scenario_all" have to be added to the "tags" object.
```
"""

__author__ = "Marcus Meeßen"
__copyright__ = "Copyright (C) 2019 MASCOR Institute"
__version__ = "1.0"

import re
from typing import List, Set

from docutils import nodes
from docutils.nodes import Admonition, Element, General, Inline, Node, \
    TextElement
from docutils.parsers.rst import directives
from docutils.parsers.rst.directives.admonitions import BaseAdmonition
from sphinx.application import Sphinx
from sphinx.directives import Only
from sphinx.errors import ExtensionError
from sphinx.writers.html import HTMLTranslator


# noinspection PyPep8Naming
class strike(Inline, TextElement):
    pass


def visit_strike_html(self: HTMLTranslator, _node) -> None:
    self.body.append('<s>')


def depart_strike_html(self: HTMLTranslator, _node) -> None:
    self.body.append('</s>')


def visit_strike_latex(_self, _node) -> None:
    pass


def depart_strike_latex(_self, _node) -> None:
    pass


# noinspection PyPep8Naming
class task(Admonition, Element):
    pass


def visit_task_html(self: HTMLTranslator, node: task) -> None:
    self.body.append('<div class="admonition task warning">')
    node.insert(0, nodes.title('task', 'Task'))
    self.set_first_last(node)


def depart_task_html(self: HTMLTranslator, _node) -> None:
    self.body.append('</div>')


def visit_task_latex(_self, _node) -> None:
    pass


def depart_task_latex(_self, _node) -> None:
    pass


class Task(BaseAdmonition):
    node_class = task


# noinspection PyPep8Naming
class internal(Admonition, Element):
    pass


def visit_internal_html(self: HTMLTranslator, node: internal) -> None:
    self.body.append('<div class="admonition note internal">')
    node.insert(0, nodes.title('internal-note', 'Internal Note'))
    self.set_first_last(node)


def depart_internal_html(self: HTMLTranslator, _node) -> None:
    self.body.append('</div>')


def visit_internal_latex(_self, _node) -> None:
    pass


def depart_internal_latex(_self, _node) -> None:
    pass


class Internal(BaseAdmonition):
    node_class = internal
    enabled: bool = False

    def run(self) -> List[Node]:
        return super().run() if Internal.enabled is True else []


# noinspection PyPep8Naming
class level(General, Element):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.levels: Set[str] = set()


def visit_level_html(self: HTMLTranslator, node: level) -> None:
    self.body.append(
        '<div class="level"><div><div class="level-badges">%s</div><div>'
        % ''.join(['<span class="level-label">%s</span>' % label
                   for label in node.levels])
    )
    self.set_first_last(node)


def depart_level_html(self: HTMLTranslator, _node) -> None:
    self.body.append('</div></div><div class="level-bar"></div></div>')


def visit_level_latex(_self, _node) -> None:
    pass


def depart_level_latex(_self, _node) -> None:
    pass


class Level(Only):
    option_spec = {'raw': directives.class_option}

    def run(self) -> List[Node]:
        only = super().run()[0]
        node = level()
        node.levels = self.options['raw']
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
        % ''.join(['<span class="scenario-label">%s</span>' % label
                   for label in node.scenarios])
    )
    self.set_first_last(node)


def depart_scenario_html(self: HTMLTranslator, _node) -> None:
    self.body.append('</div></div><div class="scenario-bar"></div></div>')


def visit_scenario_latex(_self, _node) -> None:
    pass


def depart_scenario_latex(_self, _node) -> None:
    pass


class Scenario(Only):
    option_spec = {'raw': directives.class_option}

    def run(self) -> List[Node]:
        only = super().run()[0]
        node = scenario()
        node.scenarios = self.options['raw']
        only.children, node.children = node, only.children
        return [only]


def generate_expression(topic: str, directive: str, original: str) -> str:
    invalid_keywords = re.search(r'(all|not|and|or|is|True|False|None)',
                                 original)
    if invalid_keywords is not None:
        raise ExtensionError("Invalid keyword '%s' in %s expression."
                             % (invalid_keywords.group(1), directive))

    selectors: List[str] = re.split(r'[ \n]+', original)

    if directive == 'level':
        valid_levels: List[str] = ['beginner', 'intermediate', 'advanced']

        if not all(selector in valid_levels for selector in selectors):
            raise ExtensionError("Invalid expression '%s' in level directive, "
                                 "allowed specifiers are %s."
                                 % (original, valid_levels))

    selectors += ['all']

    for index, selector in enumerate(selectors):
        selectors[index] = '%s_%s_%s or all_%s_%s' \
                           % (topic, directive, selector,
                              directive, selector)

    return ' or '.join(selectors)


def process_selectors(_app, _doc_name, source: List[str]) -> None:
    if not len(source) > 0:
        raise ExtensionError("Could not process an empty source list.")

    meta = re.match(r'^\.\. meta::\n[ ]{3}:topic: ([\w\-]+)', source[0])

    if not meta:
        return  # file is not compatible with selectors

    line_groups: List[str] = re.split(r'(\n{2,})', source[0])
    topic: str = meta.group(1)

    for index, line_group in enumerate(line_groups):
        line_groups[index] = re.sub(
            r'^(([ ]*)\.\. (level|scenario):: )([\n\w\- ]+)',
            lambda x: '%s%s\n%s   :raw: %s' % (x.group(1),
                                               generate_expression(topic,
                                                                   x.group(3),
                                                                   x.group(4)),
                                               x.group(2),
                                               re.sub(r'\n', ' ', x.group(4))),
            line_group)

    source[0] = str().join(line_groups)


def setup(app: Sphinx):
    if 'internal' in app.tags:
        Internal.enabled = True

    app.add_stylesheet('style/didactic.css')
    app.add_node(strike,
                 html=(visit_strike_html, depart_strike_html),
                 latex=(visit_strike_latex, depart_strike_latex))
    app.add_node(task,
                 html=(visit_task_html, depart_task_html),
                 latex=(visit_task_latex, depart_task_latex))
    app.add_node(internal,
                 html=(visit_internal_html, depart_internal_html),
                 latex=(visit_internal_latex, depart_internal_latex))
    app.add_node(level,
                 html=(visit_level_html, depart_level_html),
                 latex=(visit_level_latex, depart_level_latex))
    app.add_node(scenario,
                 html=(visit_scenario_html, depart_scenario_html),
                 latex=(visit_scenario_latex, depart_scenario_latex))
    app.add_generic_role('strike', strike)
    app.add_directive('task', Task)
    app.add_directive('internal', Internal)
    app.add_directive('level', Level)
    app.add_directive('scenario', Scenario)
    app.connect('source-read', process_selectors)
