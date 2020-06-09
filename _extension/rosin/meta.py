# Copyright (C) 2019-2020 MASCOR Institute. All rights reserved.

"""
The rosin.Meta is an extension of Sphinx, which allows to show or completely
hide a single document and to add further attributes to it. For this purpose,
firstly, the unit's filename is used, which must be present in the configured
`tags` in order for it to be included in the assembled package, and secondly,
the `meta` directive is enhanced to interpret the needed attributes.

Example:
`conf.py`
```
tags.add('my_document')
```

`my_document.rst`
```
.. meta::
   :unit-type: ( lecture | tutorial | workshop | narrative )
   :unit-interaction: ( theory | mixed | practice )
   :unit-duration: { ( all | beginner | intermediate | advanced ) / time }
   :unit-requires: { ( unit_filename | descriptor ) , }
   :unit-mentions: { ( unit_filename | descriptor ) , }
   :unit-provides: { descriptor , }
```

-  `:unit-requires:` is automatically generated from every `:r-term:`,
   `:r-program:`, and `:r-option:` role used in a document
-  `:unit-mentions:` is automatically generated from every `:term:`,
   `:program:`, and `:option:` role used in a document
-  `:unit-provides:` is automatically generated from the glossary and program
    entries that were defined in the document

Known Issues:
-  A document that has been removed once will not show up in TOCs anymore even
   if it has been added again. The current workaround is to delete the build
   folder or to run `make clean`.
"""

__author__ = "Meeßen, Marcus"
__copyright__ = "Copyright (C) 2019-2020 MASCOR Institute"
__version__ = "2.0"

import os
import re
from typing import Dict, List, Match, Set, Union

from docutils.nodes import Node, Text, document, inline, option, reference, \
    strong, term
from docutils.parsers.rst import Directive
from docutils.parsers.rst.directives.body import Sidebar
from sphinx import addnodes
from sphinx.application import Sphinx
from sphinx.config import Config
from sphinx.errors import ExtensionError
from sphinx.util import logging

UNIT_TYPE: Set[str] = {'lecture', 'tutorial', 'workshop', 'narrative'}
UNIT_INTERACTION: Set[str] = {'theory', 'mixed', 'practice'}
UNIT_DURATION_LEVEL: Set[str] = {'all', 'beginner', 'intermediate', 'advanced'}

logger = logging.getLogger(__name__)

unused_docs: Set[str] = set()
required_docs: Set[str] = set()
mentioned_docs: Set[str] = set()


class MetaDoc(object):
    @staticmethod
    def builder_inited(app: Sphinx) -> None:
        app.builder.read()  # reread all files
        app.env.found_docs.difference_update(unused_docs)

    @staticmethod
    def config_inited(app: Sphinx, config: Config) -> None:
        global unused_docs, required_docs, mentioned_docs

        found_docs: List[str] = []
        for root, _, files in os.walk(os.curdir):
            for file in files:
                if file.endswith(".rst"):
                    found_docs.append(os.path.splitext(os.path.relpath(
                        os.path.join(root, file), start=os.curdir))[0])

        # collect meta data
        required_by: Dict[str, Set[str]] = {}
        mentioned_by: Dict[str, Set[str]] = {}
        provided_by: Dict[str, str] = {}
        course_docs: Set[str] = set()
        for doc in found_docs:
            filename: str = '%s.rst' % doc

            if not os.path.isfile(filename):
                logger.warning("Document '%s' may contain meta information "
                               "that cannot be handled by the rosin.Meta "
                               "extension." % filename)
                continue

            if config.hex_hash(doc) in app.tags:
                course_docs.add(doc)

            provided_by[doc] = doc

            def new_provided_by(doc_name: str, value: str):
                if value in provided_by and doc_name != provided_by[value]:
                    logger.warning("Document '%s' provides '%s' which is "
                                   "already done by '%s'."
                                   % (doc_name, value, provided_by[value]))
                else:
                    provided_by[value] = doc

            def new_required_by(doc_name: str, value: str):
                required_by.setdefault(value, set())
                required_by[value].add(doc_name)

            def new_mentioned_by(doc_name: str, value: str):
                mentioned_by.setdefault(value, set())
                mentioned_by[value].add(doc_name)

            with open(filename, 'r') as file:
                content: str = file.read()

                # collect meta directive from document
                meta: Union[str, None] = None
                for line in content.split('\n'):
                    if line.startswith('.. meta::'):
                        meta = ''
                    elif meta is not None:
                        if not line.strip():
                            pass  # empty lines between options are okay
                        elif not line.startswith('   '):
                            break  # leaving the meta directives body
                        else:
                            meta += line

                # create a comma-separated list of tokens in the meta directive
                if meta is None:
                    logger.warning("Document '%s' does not contain a meta "
                                   "directive." % filename)
                else:
                    for substitution in [
                        (r'[\t\n\r\f\v]', r' '),  # remove special whitespace
                        (r'((: )|( :))', r'\2,\3'),  # tokenize options
                        (r' +', r' '),  # remove multiple spaces
                        (r'( )?,( )?', r','),  # remove space around tokens
                    ]:
                        pattern, replace = substitution
                        meta = re.sub(pattern, replace, meta)

                # parse meta options and save them in the app environment
                state: Union[str, None] = None
                for token in (meta.split(',') if meta is not None else []):
                    token = token.strip()
                    if state is not None and not token.startswith(':'):
                        pass
                    elif token in [
                        ':unit-type:',
                        ':unit-interaction:',
                        ':unit-duration:',
                        ':unit-requires:',
                        ':unit-mentions:',
                        ':unit-provides:',
                    ]:
                        state = token
                    else:
                        state = None

                    if state is None or token.startswith(':'):
                        continue
                    elif state == ':unit-type:':
                        if token not in UNIT_TYPE:
                            raise ExtensionError("Invalid token '%s' in option "
                                                 ":unit-type:, allowed tokens "
                                                 "are %s." % (token, UNIT_TYPE))
                        pass  # currently unused
                    elif state == ':unit-interaction:':
                        if token not in UNIT_INTERACTION:
                            raise ExtensionError("Invalid token '%s' in option "
                                                 ":unit-interaction:, allowed "
                                                 "tokens are %s."
                                                 % (token, UNIT_INTERACTION))
                        pass  # currently unused
                    elif state == ':unit-duration:':
                        try:
                            level, time = token.split('/')
                        except ValueError:
                            raise ExtensionError("Invalid token '%s' in option "
                                                 ":unit-duration:, format as "
                                                 "'<level>/<time>'." % token)
                        if not time.isdigit():
                            raise ExtensionError("Invalid token '%s' in option "
                                                 ":unit-duration:, time is not "
                                                 "an integer." % token)
                        if level not in UNIT_DURATION_LEVEL:
                            raise ExtensionError("Invalid token '%s' in option "
                                                 ":unit-duration:, allowed "
                                                 "levels are %s."
                                                 % (token, UNIT_DURATION_LEVEL))
                        pass  # currently unused
                    elif state == ':unit-requires:':
                        new_required_by(doc, token)
                    elif state == ':unit-mentions:':
                        new_mentioned_by(doc, token)
                    elif state == ':unit-provides:':
                        new_provided_by(doc, token)
                    else:
                        pass

                # find required and mentioned terms, programs, and options
                for find in re.findall(r'(?<!`):(r-)?(term|program|option):'
                                       r'`([^`]+)`(?!`)', content):
                    required, role, enclosed = find
                    enclosed = re.sub(r'[\t\n\r\f\v]', r' ', enclosed)
                    enclosed = re.sub(r' +', r' ', enclosed)
                    pair = "%s:%s" % (role, enclosed.lower())
                    if required:
                        new_required_by(doc, pair)
                    else:
                        new_mentioned_by(doc, pair)

                # find provided programs and options
                program: Union[str, None] = None
                for find in re.findall(r'(?<!`).. (program|option):: '
                                       r'(.+)(?:\n\n)', content):
                    role, enclosed = find
                    enclosed = re.sub(r'[\t\n\r\f\v]', r' ', enclosed)
                    enclosed = re.sub(r' +', r' ', enclosed)

                    if role == "program":
                        program = enclosed
                        pair = "%s:%s" % (role, enclosed.lower())
                    elif program is not None:
                        pair = "%s:%s %s" % (role, program, enclosed.lower())
                    else:
                        logger.warning("No program defined before option "
                                       "directive is used.")
                        continue

                    new_provided_by(doc, pair)

                # find provided terms from glossaries
                glossary_indent: Union[int, None] = None
                for line in content.split('\n'):
                    glossary_match: Match = re.match(r'(( {3})*).. glossary::',
                                                     line)
                    if glossary_match is not None:
                        glossary_indent = len(glossary_match.group(1))
                    elif glossary_indent is not None:
                        entry_match: Match = re.match(r'(( {3})*)([^ ].*)',
                                                      line)
                        if entry_match is not None:
                            indent, _, enclosed = entry_match.groups()
                            enclosed = re.sub(r'[\t\n\r\f\v]', r' ', enclosed)
                            enclosed = re.sub(r' +', r' ', enclosed)
                            if len(indent) == glossary_indent + 3:
                                # remove comments, options, and grouping keys
                                entry: str = re.sub(r'(:strike:|:sorted:|`'
                                                    r'|\.\..*| : .*)',
                                                    '', enclosed)
                                if entry:
                                    pair = 'term:%s' % entry.lower()
                                    new_provided_by(doc, pair)

                            elif len(indent) < glossary_indent + 3:
                                glossary_indent = None  # end of the directive
                            else:
                                pass  # definitions

        # solve soft or "mentioned" and hard or "required" document dependencies
        for is_referenced, referenced_by in [
            (required_docs, required_by),
            # required references are more important than mentioned ones
            (mentioned_docs, mentioned_by),
        ]:
            # remove unsatisfiable references
            for missing in [referenced
                            for referenced in referenced_by.keys()
                            if referenced not in provided_by]:
                logger.warning("Document(s) %s uses '%s' which is not provided "
                               "by any other document."
                               % (referenced_by[missing], missing))
                referenced_by.pop(missing)
            # stop when no change to the set of tagged documents is made
            tagged: Set[str] = course_docs.copy()
            changed: bool = True
            while changed:
                changed = False
                for referenced, by in referenced_by.items():
                    if all(by not in tagged for by in by):
                        continue
                    if provided_by[referenced] not in tagged:
                        tagged.add(provided_by[referenced])
                        is_referenced.add(provided_by[referenced])
                        changed = True

        mentioned_docs.difference_update(required_docs)

        for doc in found_docs:
            if all(doc not in docs for docs in [
                course_docs,
                required_docs,
                mentioned_docs,
            ]):
                unused_docs.add(doc)

    @staticmethod
    def env_get_outdated(_app, _env, added: Set[str], changed: Set[str],
                         removed: Set[str]) -> List[str]:
        added.difference_update(unused_docs)
        changed.difference_update(unused_docs)
        removed.update(unused_docs)
        return []

    @staticmethod
    def doc_tree_read(_app, doc_tree: document) -> None:
        for toc_tree in doc_tree.traverse(addnodes.toctree):
            for entry in toc_tree['entries']:
                if entry[1] in unused_docs:
                    toc_tree['entries'].remove(entry)


class DocumentInfo(Sidebar):
    required_arguments: int = 0
    has_content: bool = True

    def run(self) -> List[Node]:
        self.arguments = ["Document Info"]
        sidebar_node = super().run()[0]
        for required_doc in required_docs:
            reference_node = reference('', '',
                                       internal=False,
                                       refuri=required_doc,
                                       anchorname='',
                                       *[Text(required_doc)]
                                       )
            inline_node = inline()
            inline_node.append(reference_node)
            sidebar_node.append(inline_node)
        return [sidebar_node]


class TOCTreeRequired(Directive):
    def run(self) -> List[Node]:
        toc_tree_node = addnodes.toctree(
            entries=[('', required_doc)
                     for required_doc in required_docs],
            glob=False,
            includefiles=[],
        )

        return [toc_tree_node]


class TOCTreeMentioned(Directive):
    def run(self) -> List[Node]:
        toc_tree_node = addnodes.toctree(
            entries=[('', mentioned_doc)
                     for mentioned_doc in mentioned_docs],
            glob=False,
            includefiles=[],
        )

        return [toc_tree_node]


def setup(app: Sphinx) -> None:
    app.ignore = []
    if 'hex_hash' not in app.config:
        app.add_config_value('hex_hash', None, 'env')
    app.connect('builder-inited', MetaDoc.builder_inited)
    app.connect('config-inited', MetaDoc.config_inited)
    app.connect('env-get-outdated', MetaDoc.env_get_outdated)
    app.connect('doc''tree-read', MetaDoc.doc_tree_read)
    app.add_directive('toc''tree_required', TOCTreeRequired)
    app.add_directive('toc''tree_mentioned', TOCTreeMentioned)
    app.add_directive('document_info', DocumentInfo)
    app.add_generic_role('r-term', term)
    app.add_generic_role('r-program', strong)
    app.add_generic_role('r-option', option)
