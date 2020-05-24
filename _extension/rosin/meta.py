# Copyright (C) 2019 MASCOR Institute. All rights reserved.

"""
The rosin.Meta is an extension of Sphinx that allows to completely hide an
individual document. For this purpose the `meta` directive is enhanced so that
tags from the configuration can be used to enable a single document.

Example:
`conf.py`
```
tags.add('my_topic')
```
`my_document.rst`
```
.. meta::
  :topic: my_topic
```

Known Issues:
-  A document that has been removed once will not show up in TOCs anymore even
   if it has been added again. The current workaround is to delete the build
   folder or to run `make clean`.
"""

__author__ = "Marcus Meeßen"
__copyright__ = "Copyright (C) 2019 MASCOR Institute"
__version__ = "1.0"

import os
import re
from typing import List, Set

from docutils import nodes
from sphinx import addnodes
from sphinx.application import Sphinx


class MetaDoc(object):
    def __init__(self) -> None:
        self.unused_docs: Set[str] = set()

    def builder_inited(self, app: Sphinx) -> None:
        for doc in app.env.found_docs:
            filename: str = '%s%s%s.rst' % (app.env.srcdir, os.sep, doc)
            meta_directive: str

            if not os.path.isfile(filename):
                continue

            with open(filename, 'r') as file:
                meta_directive = file.readline() + file.readline()

            if meta_directive is not None:
                meta_topic = re.match(r'^\.\. meta::\n[ ]{3}:topic: ([\w\-]+)',
                                      meta_directive)
                if meta_topic is not None:
                    if meta_topic.group(1) not in app.tags:
                        self.unused_docs.add(doc)
                    else:
                        app.env.metadata[doc]['topic'] = meta_topic.group(1)
                else:
                    return  # the file does not use the meta topic system

        app.env.found_docs.difference_update(self.unused_docs)

    def env_get_outdated(self, _app, _env, added: Set[str], changed: Set[str],
                         removed: Set[str]) -> List[str]:
        added.difference_update(self.unused_docs)
        changed.difference_update(self.unused_docs)
        removed.update(self.unused_docs)
        return []

    def doc_tree_read(self, _app, doc_tree: nodes.document) -> None:
        for toc_tree in doc_tree.traverse(addnodes.toctree):
            for entry in toc_tree['entries']:
                if entry[1] in self.unused_docs:
                    toc_tree['entries'].remove(entry)


def setup(app: Sphinx) -> None:
    meta_doc: MetaDoc = MetaDoc()
    app.ignore = []
    app.connect('builder-inited', meta_doc.builder_inited)
    app.connect('env-get-outdated', meta_doc.env_get_outdated)
    app.connect('doctree-read', meta_doc.doc_tree_read)
