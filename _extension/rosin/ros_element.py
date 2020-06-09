# Copyright (C) 2019-2020 MASCOR Institute. All rights reserved.

"""
The rosin.ROS_Element extension of Sphinx provides several text roles to
highlight the different elements of the Robot Operating System. The `:ros:`
domain includes roles for package, node, message, service, action, topic, and
parameter. There are also some suffixes to indicate whether the element is part
of the official ROS release, or to determine the belonging of an element to
another package/node. For official packages, messages, actions, and services
links to the official documentation will be automatically generated. Some roles
require more then one parameter, e.g. a node also requires a package. This
information will be used to generate a "hierarchy" like "Package/Node". Place a
"short" before the other parameters to omit this behaviour. See the example
below for further information.

Example:
```
All text roles:
-  :ros:package:`official_package`
-  :ros:package-i:`local_package`
-  :ros:node:`official_node official_package`
-  :ros:node-i:`local_node local_package`
-  :ros:message:`official_message official_package`
-  :ros:message-i:`local_message local_package`
-  :ros:service:`official_service official_package`
-  :ros:service-i:`local_service local_package`
-  :ros:action:`official_action official_package`
-  :ros:action-i:`local_action local_package`
-  :ros:topic:`official_topic`
-  :ros:topic-i:`local_topic`
-  :ros:topic-np:`official_topic official_node official_package`
-  :ros:topic-inp:`local_topic local_node local_package`
-  :ros:parameter:`official_parameter`
-  :ros:parameter-i:`local_parameter`
-  :ros:parameter-np:`official_parameter official_node official_package`
-  :ros:parameter-inp:`local_parameter local_node local_package`

Short variants:
-  :ros:parameter-np:`parameter node package` will print package/node/parameter.
-  :ros:parameter-np:`parameter node short package` will print node/parameter.
-  :ros:parameter-np:`parameter short node package` will print parameter.
-  ... and all other roles with more than one parameter.
´´´
"""

__author__ = "Meeßen, Marcus"
__copyright__ = "Copyright (C) 2019-2020 MASCOR Institute"
__version__ = "1.2"

import re
from typing import Dict, List, Tuple

from docutils.nodes import Inline, Node, TextElement, reference
from sphinx.application import Sphinx
from sphinx.config import Config
from sphinx.domains import Domain
from sphinx.errors import ExtensionError
from sphinx.writers.html import HTMLTranslator
from sphinx.writers.latex import LaTeXTranslator


# noinspection PyPep8Naming
class index_text(Inline, TextElement):
    pass


def visit_index_text_html(self: HTMLTranslator, node: index_text) -> None:
    self.body.append('<span style="color: rgb(%d, %d, %d);">'
                     % (*ROSDomain.index_color,))
    self.visit_superscript(node)
    self.visit_emphasis(node)


def depart_index_text_html(self: HTMLTranslator, node: index_text) -> None:
    self.depart_emphasis(node)
    self.depart_superscript(node)
    self.body.append('</span>')


def visit_index_text_latex(self: LaTeXTranslator, node: index_text) -> None:
    self.body.append('\\text''color[RGB]{%d,%d,%d}{'
                     % (*ROSDomain.index_color,))
    self.visit_superscript(node)
    self.visit_emphasis(node)


def depart_index_text_latex(self: LaTeXTranslator, node: index_text) -> None:
    self.depart_emphasis(node)
    self.depart_superscript(node)
    self.body.append('}')


# noinspection PyPep8Naming
class literal_text(Inline, TextElement):
    pass


def visit_literal_text_html(self: HTMLTranslator, node: literal_text) -> None:
    self.body.append('<code class="%s" style="background: rgb(%d, %d, %d);'
                     ' color: rgb(%d, %d, %d);">'
                     % (' '.join(node.attributes['classes']),
                        *ROSDomain.box_color,
                        *node.attributes['text_color']))


def depart_literal_text_html(self: HTMLTranslator, _node) -> None:
    self.body.append('</code>')


def visit_literal_text_latex(self: LaTeXTranslator, node: literal_text) -> None:
    self.body.append('\\color''box[RGB]{%d,%d,%d}{'
                     '\\v''phantom{Ay}'
                     '\\text''color[RGB]{%d,%d,%d}{'
                     '\\sphinx''code{'
                     % (*ROSDomain.box_color,
                        *node.attributes['text_color']))


def depart_literal_text_latex(self: LaTeXTranslator, _node) -> None:
    self.body.append('}}}')


# noinspection PyPep8Naming
class titled_text(Inline, TextElement):
    pass


def visit_titled_text_html(self: HTMLTranslator, node: titled_text) -> None:
    self.body.append('<span title="%s">'
                     % self.attval(node.attributes['title']))


def depart_titled_text_html(self: HTMLTranslator, _node) -> None:
    self.body.append('</span>')


def visit_titled_text_latex(_self, _node) -> None:
    pass


def depart_titled_text_latex(_self, _node) -> None:
    pass


class ROSComponent(object):
    def __init__(self, parts: List[str] = None, uri: str = None,
                 classes: List[str] = None, index: str = None,
                 text_color: Tuple[int, int, int] = (0, 0, 0)) -> None:
        self.parts: List[str] = parts if parts is not None else []
        self.uri: str = uri
        self.classes: List[str] = classes if classes is not None else []
        self.index = index
        self.text_color: Tuple[int, int, int] = text_color

    def __call__(self, _name, raw_text: str, text: str,
                 *args, **kwargs) -> Tuple[List[Node], List[Node]]:
        texts: List[str] = re.split(r'[ \n]+', text)
        parts_without_suffixes: List[str] = [part.split('-')[0]
                                             for part in self.parts]

        if not len(texts) == len(parts_without_suffixes):
            raise ExtensionError("ROS element has an incompatible number of "
                                 "tokens. Expected %s, but got %s."
                                 % (parts_without_suffixes, texts))

        literal_node = literal_text(
            rawsource=raw_text,
            text_color=self.text_color,
            text=texts[0],
            classes=['xref', 'pre', 'ros'] + self.classes,
        )

        if self.index is not None:
            index_node = index_text(
                text=self.index,
            )
            literal_node.append(index_node)

        titled_node = titled_text(
            title="ROS %s" % " from ".join(
                ["%s ""%s""" % (part, text)
                 for part, text in zip(parts_without_suffixes, texts)]),
            rawsource=raw_text,
        )
        titled_node.append(literal_node)

        if self.uri is None:
            return [titled_node], []
        else:
            reference_node = reference(
                rawsource=raw_text,
                refuri=self.uri % dict(zip(self.parts, texts)),
                target='_blank',
            )
            reference_node.append(titled_node)

            return [reference_node], []


class ROSDomain(Domain):
    name: str = 'ros'
    label: str = "Robot Operating System"
    release_uri: str = 'https://docs.ros.org/melodic/api/'
    box_color: Tuple[int, int, int]
    index_color: Tuple[int, int, int]
    roles: Dict[str, ROSComponent] = {
        'package': ROSComponent(
            parts=['package'],
            uri='https://wiki.ros.org/%(package)s',
            classes=['ros-package'],
        ),
        'package-i': ROSComponent(
            parts=['package-i'],
            classes=['ros-package-i'],
            index='i',
        ),
        'node': ROSComponent(
            parts=['node', 'package'],
            classes=['ros-node'],
        ),
        'node-i': ROSComponent(
            parts=['node-i', 'package-i'],
            classes=['ros-node-i'],
            index='i',
        ),
        'message': ROSComponent(
            parts=['message', 'package'],
            uri='%s%%(package)s/html/msg/%%(message)s.html' % release_uri,
            classes=['ros-message'],
            index='m',
        ),
        'message-i': ROSComponent(
            parts=['message-i', 'package-i'],
            classes=['ros-message-i'],
            index='mi',
        ),
        'service': ROSComponent(
            parts=['service', 'package'],
            uri='%s%%(package)s/html/srv/%%(service)s.html' % release_uri,
            classes=['ros-service'],
            index='s',
        ),
        'service-i': ROSComponent(
            parts=['service-i', 'package-i'],
            classes=['ros-service-i'],
            index='si',
        ),
        'action': ROSComponent(
            parts=['action', 'package'],
            uri='%s%%(package)s/html/action/%%(action)s.html' % release_uri,
            classes=['ros-action'],
            index='a',
        ),
        'action-i': ROSComponent(
            parts=['action-i', 'package-i'],
            classes=['ros-action-i'],
            index='ai',
        ),
        'topic': ROSComponent(
            parts=['topic'],
            classes=['ros-topic'],
        ),
        'topic-i': ROSComponent(
            parts=['topic-i'],
            classes=['ros-topic-i'],
            index='i',
        ),
        'topic-np': ROSComponent(
            parts=['topic-np', 'node', 'package'],
            classes=['ros-topic'],
        ),
        'topic-inp': ROSComponent(
            parts=['topic-inp', 'node-i', 'package-i'],
            classes=['ros-topic-i'],
            index='i',
        ),
        'parameter': ROSComponent(
            parts=['parameter'],
            classes=['ros-parameter'],
        ),
        'parameter-i': ROSComponent(
            parts=['parameter-i'],
            classes=['ros-parameter-i'],
            index='i',
        ),
        'parameter-np': ROSComponent(
            parts=['parameter-np', 'node', 'package'],
            classes=['ros-parameter'],
        ),
        'parameter-inp': ROSComponent(
            parts=['parameter-inp', 'node-i', 'package-i'],
            classes=['ros-parameter-i'],
            index='i',
        ),
    }

    # noinspection SpellCheckingInspection
    def merge_domaindata(self, *args, **kwargs) -> None:
        pass

    # noinspection SpellCheckingInspection
    def resolve_any_xref(self, *args, **kwargs) -> List[Tuple[str, Node]]:
        pass


def divide_parts(parts: List[str], texts: List[str]) -> List[str]:
    if len(texts) == 0 or len(parts) == 0 or texts[0] == 'short':
        return []

    texts_without_short: List[str] = [text
                                      for text in texts
                                      if text != 'short']

    role_with_texts: str = ':ros:%s:`%s`' % (parts[0],
                                             ' '.join(texts_without_short))

    return divide_parts(parts[1:], texts[1:]) + [role_with_texts]


def process_comm(_app, _doc_name, source: List[str]) -> None:
    if not len(source) > 0:
        raise ExtensionError("Could not process an empty source list.")

    source[0]: str = re.sub(
        # this regex is currently not safe for code blocks, but for inline code
        # if the role is adjacent to a grave accent on at least one side
        r'(?<!`):ros:(%s):`([a-zA-Z_ \n]+)`(?!`)'
        % '|'.join(ROSDomain.roles.keys()),
        lambda x: '/'.join(divide_parts(ROSDomain.roles[x.group(1)].parts,
                                        re.split(r'[ \n]+', x.group(2)))),
        source[0]
    )


def config_inited(_app, config: Config) -> None:
    ROSDomain.box_color = config['ros_element_box_color']
    ROSDomain.index_color = config['ros_element_index_color']

    for key, roles in [
        ('ros_element_package_color', ['package', 'package-i']),
        ('ros_element_node_color', ['node', 'node-i']),
        ('ros_element_message_color', ['message', 'message-i']),
        ('ros_element_service_color', ['service', 'service-i']),
        ('ros_element_action_color', ['action', 'action-i']),
        ('ros_element_topic_color', ['topic', 'topic-i',
                                     'topic-np', 'topic-inp']),
        ('ros_element_parameter_color', ['parameter', 'parameter-i',
                                         'parameter-np', 'parameter-inp']),
    ]:
        for role in roles:
            ROSDomain.roles[role].text_color = config[key]


def setup(app: Sphinx) -> None:
    app.add_config_value('ros_element_index_color', (112, 128, 144), 'env')
    app.add_config_value('ros_element_box_color', (255, 255, 224), 'env')
    app.add_config_value('ros_element_package_color', (0, 100, 0), 'env')
    app.add_config_value('ros_element_node_color', (65, 105, 225), 'env')
    app.add_config_value('ros_element_message_color', (255, 69, 0), 'env')
    app.add_config_value('ros_element_service_color', (255, 69, 0), 'env')
    app.add_config_value('ros_element_action_color', (255, 69, 0), 'env')
    app.add_config_value('ros_element_topic_color', (160, 32, 240), 'env')
    app.add_config_value('ros_element_parameter_color', (47, 79, 79), 'env')

    app.add_domain(ROSDomain)
    app.add_stylesheet('style/ros_element.css')
    app.add_node(index_text,
                 html=(visit_index_text_html, depart_index_text_html),
                 latex=(visit_index_text_latex, depart_index_text_latex),
                 )
    app.add_node(literal_text,
                 html=(visit_literal_text_html, depart_literal_text_html),
                 latex=(visit_literal_text_latex, depart_literal_text_latex),
                 )
    app.add_node(titled_text,
                 html=(visit_titled_text_html, depart_titled_text_html),
                 latex=(visit_titled_text_latex, depart_titled_text_latex),
                 )
    app.connect('source-read', process_comm)
    app.connect('config-inited', config_inited)
