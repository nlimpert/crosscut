# Copyright (C) 2019 MASCOR Institute. All rights reserved.

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

__author__ = "Marcus Meeßen"
__copyright__ = "Copyright (C) 2019 MASCOR Institute"
__version__ = "1.0"

import re
from typing import Dict, List, Tuple

from docutils.nodes import Inline, Node, TextElement, literal, reference
from sphinx.application import Sphinx
from sphinx.domains import Domain
from sphinx.errors import ExtensionError
from sphinx.writers.html import HTMLTranslator


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
                 classes: List[str] = None) -> None:
        self.parts: List[str] = parts if parts is not None else []
        self.uri: str = uri
        self.classes: List[str] = classes if classes is not None else []

    def __call__(self, _name, raw_text: str, text: str,
                 *args, **kwargs) -> Tuple[List[Node], List[Node]]:
        texts: List[str] = re.split(r'[ \n]+', text)
        parts_without_suffixes: List[str] = [part.split('-')[0]
                                             for part in self.parts]

        if not len(texts) == len(parts_without_suffixes):
            raise ExtensionError("ROS element has an incompatible number of "
                                 "tokens. Expected %s, but got %s."
                                 % (parts_without_suffixes, texts))

        literal_node = literal(
            rawsource=raw_text,
            text=texts[0],
            classes=['xref', 'ros'] + self.classes,
        )

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
    roles: Dict[str, ROSComponent] = {
        'package': ROSComponent(
            parts=['package'],
            uri='https://wiki.ros.org/%(package)s',
            classes=['ros-package'],
        ),
        'package-i': ROSComponent(
            parts=['package-i'],
            classes=['ros-package-i'],
        ),
        'node': ROSComponent(
            parts=['node', 'package'],
            classes=['ros-node'],
        ),
        'node-i': ROSComponent(
            parts=['node-i', 'package-i'],
            classes=['ros-node-i'],
        ),
        'message': ROSComponent(
            parts=['message', 'package'],
            uri='%s%%(package)s/html/msg/%%(message)s.html' % release_uri,
            classes=['ros-message'],
        ),
        'message-i': ROSComponent(
            parts=['message-i', 'package-i'],
            classes=['ros-message-i'],
        ),
        'service': ROSComponent(
            parts=['service', 'package'],
            uri='%s%%(package)s/html/srv/%%(service)s.html' % release_uri,
            classes=['ros-service'],
        ),
        'service-i': ROSComponent(
            parts=['service-i', 'package-i'],
            classes=['ros-service-i'],
        ),
        'action': ROSComponent(
            parts=['action', 'package'],
            uri='%s%%(package)s/html/action/%%(action)s.html' % release_uri,
            classes=['ros-action'],
        ),
        'action-i': ROSComponent(
            parts=['action-i', 'package-i'],
            classes=['ros-action-i'],
        ),
        'topic': ROSComponent(
            parts=['topic'],
            classes=['ros-topic'],
        ),
        'topic-i': ROSComponent(
            parts=['topic-i'],
            classes=['ros-topic-i'],
        ),
        'topic-np': ROSComponent(
            parts=['topic-np', 'node', 'package'],
            classes=['ros-topic'],
        ),
        'topic-inp': ROSComponent(
            parts=['topic-inp', 'node-i', 'package-i'],
            classes=['ros-topic-i'],
        ),
        'parameter': ROSComponent(
            parts=['parameter'],
            classes=['ros-parameter'],
        ),
        'parameter-i': ROSComponent(
            parts=['parameter-i'],
            classes=['ros-parameter-i'],
        ),
        'parameter-np': ROSComponent(
            parts=['parameter-np', 'node', 'package'],
            classes=['ros-parameter'],
        ),
        'parameter-inp': ROSComponent(
            parts=['parameter-inp', 'node-i', 'package-i'],
            classes=['ros-parameter-i'],
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
        r':ros:(%s):`([a-zA-Z_ \n]+)`' % '|'.join(ROSDomain.roles.keys()),
        lambda x: '/'.join(divide_parts(ROSDomain.roles[x.group(1)].parts,
                                        re.split(r'[ \n]+', x.group(2)))),
        source[0]
    )


def setup(app: Sphinx) -> None:
    app.add_domain(ROSDomain)
    app.add_stylesheet('style/ros_element.css')
    app.add_node(titled_text,
                 html=(visit_titled_text_html, depart_titled_text_html),
                 latex=(visit_titled_text_latex, depart_titled_text_latex),
                 )
    app.connect('source-read', process_comm)
