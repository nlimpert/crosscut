# Copyright (C) 2019 MASCOR Institute. All rights reserved.

"""
The rosin.GUI extension of Sphinx offers several GUI elements that are missing
in the vanilla version, but are useful to increase the flow of reading and
enable a faster understanding of the instructions.

Example:
```
:gui:label: or :gui:text: is the new version of the :guilabel:.

:gui:button: shows a non-clickable button.

:gui:radio: or :gui:radio-selected: are the two available states that a radio
button may have.

:gui:checkbox:, :gui:checkbox-selected:, and :gui:checkbox-intermediate: are
the three available states that a checkbox may have.

:gui:textbox: shows non-editable textbox with a fake blinking cursor.

:gui:dropdown: is a non-interactive drop-down menu.
```
"""

__author__ = "Marcus Meeßen"
__copyright__ = "Copyright (C) 2019 MASCOR Institute"
__version__ = "1.0"

from typing import List, Dict, Tuple
from docutils.nodes import Inline, Node, TextElement
from docutils.parsers.rst import Directive
from docutils.parsers.rst.roles import GenericRole
from sphinx.application import Sphinx
from sphinx.domains import Domain
from sphinx.writers.html import HTMLTranslator


# noinspection PyPep8Naming
class button(Inline, TextElement):
    pass


def visit_button_html(self: HTMLTranslator, _node) -> None:
    self.body.append('<span class="gui-button">')


def depart_button_html(self: HTMLTranslator, _node) -> None:
    self.body.append('</span>')


# noinspection PyPep8Naming
class text(Inline, TextElement):
    pass


def visit_text_html(self: HTMLTranslator, _node) -> None:
    self.body.append('<span class="gui-text">')


def depart_text_html(self: HTMLTranslator, _node) -> None:
    self.body.append('</span>')


# noinspection PyPep8Naming
class radio(Inline, TextElement):
    pass


def visit_radio_html(self: HTMLTranslator, _node) -> None:
    self.body.append('<span class="gui-radio">'
                     '<img src="data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0c'
                     'DovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIyNCIgaGVpZ2h0PS'
                     'IyNCIgdmlld0JveD0iMCAwIDI0IDI0Ij48cGF0aCBmaWxsPSJub25lIiB'
                     'kPSJNMCAwaDI0djI0SDBWMHoiLz48cGF0aCBkPSJNMTIgMkM2LjQ4IDIg'
                     'MiA2LjQ4IDIgMTJzNC40OCAxMCAxMCAxMCAxMC00LjQ4IDEwLTEwUzE3L'
                     'jUyIDIgMTIgMnptMCAxOGMtNC40MiAwLTgtMy41OC04LThzMy41OC04ID'
                     'gtOCA4IDMuNTggOCA4LTMuNTggOC04IDh6Ii8+PC9zdmc+"/>')


def depart_radio_html(self: HTMLTranslator, _node) -> None:
    self.body.append('</span>')


# noinspection PyPep8Naming
class radio_selected(Inline, TextElement):
    pass


def visit_radio_selected_html(self: HTMLTranslator, _node) -> None:
    self.body.append('<span class="gui-radio">'
                     '<img src="data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0c'
                     'DovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIyNCIgaGVpZ2h0PS'
                     'IyNCIgdmlld0JveD0iMCAwIDI0IDI0Ij48cGF0aCBmaWxsPSJub25lIiB'
                     'kPSJNMCAwaDI0djI0SDBWMHoiLz48cGF0aCBkPSJNMTIgMkM2LjQ4IDIg'
                     'MiA2LjQ4IDIgMTJzNC40OCAxMCAxMCAxMCAxMC00LjQ4IDEwLTEwUzE3L'
                     'jUyIDIgMTIgMnptMCAxOGMtNC40MiAwLTgtMy41OC04LThzMy41OC04ID'
                     'gtOCA4IDMuNTggOCA4LTMuNTggOC04IDh6Ii8+PGNpcmNsZSBjeD0iMTI'
                     'iIGN5PSIxMiIgcj0iNSIvPjwvc3ZnPg=="/>')


def depart_radio_selected_html(self: HTMLTranslator, _node) -> None:
    self.body.append('</span>')


# noinspection PyPep8Naming
class checkbox(Inline, TextElement):
    pass


def visit_checkbox_html(self: HTMLTranslator, _node) -> None:
    self.body.append('<span class="gui-checkbox">'
                     '<img src="data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0c'
                     'DovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIyNCIgaGVpZ2h0PS'
                     'IyNCIgdmlld0JveD0iMCAwIDI0IDI0Ij48cGF0aCBmaWxsPSJub25lIiB'
                     'kPSJNMCAwaDI0djI0SDBWMHoiLz48cGF0aCBkPSJNMTkgNXYxNEg1VjVo'
                     'MTRtMC0ySDVjLTEuMSAwLTIgLjktMiAydjE0YzAgMS4xLjkgMiAyIDJoM'
                     'TRjMS4xIDAgMi0uOSAyLTJWNWMwLTEuMS0uOS0yLTItMnoiLz48L3N2Zz'
                     '4="/>')


def depart_checkbox_html(self: HTMLTranslator, _node) -> None:
    self.body.append('</span>')


# noinspection PyPep8Naming
class checkbox_selected(Inline, TextElement):
    pass


def visit_checkbox_selected_html(self: HTMLTranslator, _node) -> None:
    self.body.append('<span class="gui-checkbox">'
                     '<img src="data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0c'
                     'DovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIyNCIgaGVpZ2h0PS'
                     'IyNCIgdmlld0JveD0iMCAwIDI0IDI0Ij48cGF0aCBmaWxsPSJub25lIiB'
                     'kPSJNMCAwaDI0djI0SDBWMHoiLz48cGF0aCBkPSJNMTkgM0g1Yy0xLjEg'
                     'MC0yIC45LTIgMnYxNGMwIDEuMS45IDIgMiAyaDE0YzEuMSAwIDItLjkgM'
                     'i0yVjVjMC0xLjEtLjktMi0yLTJ6bTAgMTZINVY1aDE0djE0ek0xNy45OS'
                     'A5bC0xLjQxLTEuNDItNi41OSA2LjU5LTIuNTgtMi41Ny0xLjQyIDEuNDE'
                     'gNCAzLjk5eiIvPjwvc3ZnPg=="/>')


def depart_checkbox_selected_html(self: HTMLTranslator, _node) -> None:
    self.body.append('</span>')


# noinspection PyPep8Naming
class checkbox_indeterminate(Inline, TextElement):
    pass


def visit_checkbox_indeterminate_html(self: HTMLTranslator, _node) -> None:
    self.body.append('<span class="gui-checkbox">'
                     '<img src="data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0c'
                     'DovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIyNCIgaGVpZ2h0PS'
                     'IyNCIgdmlld0JveD0iMCAwIDI0IDI0Ij48cGF0aCBmaWxsPSJub25lIiB'
                     'kPSJNMCAwaDI0djI0SDB6Ii8+PHBhdGggZD0iTTE5IDNINWMtMS4xIDAt'
                     'MiAuOS0yIDJ2MTRjMCAxLjEuOSAyIDIgMmgxNGMxLjEgMCAyLS45IDItM'
                     'lY1YzAtMS4xLS45LTItMi0yem0wIDE2SDVWNWgxNHYxNHpNNyAxMWgxMH'
                     'YySDd6Ii8+PC9zdmc+"/>')


def depart_checkbox_indeterminate_html(self: HTMLTranslator, _node) -> None:
    self.body.append('</span>')


# noinspection PyPep8Naming
class textbox(Inline, TextElement):
    pass


def visit_textbox_html(self: HTMLTranslator, _node) -> None:
    self.body.append('<span class="gui-textbox">')


def depart_textbox_html(self: HTMLTranslator, _node) -> None:
    self.body.append('<span>&#x2758;</span></span>')


# noinspection PyPep8Naming
class dropdown(Inline, TextElement):
    pass


def visit_dropdown_html(self: HTMLTranslator, _node) -> None:
    self.body.append('<span class="gui-dropdown">')


def depart_dropdown_html(self: HTMLTranslator, _node) -> None:
    self.body.append('<img src="data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0c'
                     'DovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIyNCIgaGVpZ2h0PS'
                     'IyNCIgdmlld0JveD0iMCAwIDI0IDI0Ij48cGF0aCBvcGFjaXR5PSIuODc'
                     'iIGZpbGw9Im5vbmUiIGQ9Ik0yNCAyNEgwVjBoMjR2MjR6Ii8+PHBhdGgg'
                     'ZD0iTTE2LjU5IDguNTlMMTIgMTMuMTcgNy40MSA4LjU5IDYgMTBsNiA2I'
                     'DYtNi0xLjQxLTEuNDF6Ii8+PC9zdmc+"/>'
                     '</span>')


class GUIDomain(Domain):
    name: str = 'gui'
    label: str = "Graphical User Interface"
    roles: Dict[str, Directive] = {
        'button': GenericRole('button', button),
        'text': GenericRole('text', text),
        'label': GenericRole('label', text),
        'radio': GenericRole('radio', radio),
        'radio-selected': GenericRole('radio-selected', radio_selected),
        'checkbox': GenericRole('checkbox', checkbox),
        'checkbox-selected': GenericRole('checkbox-selected',
                                         checkbox_selected),
        'checkbox-indeterminate': GenericRole('checkbox-indeterminate',
                                              checkbox_indeterminate),
        'textbox': GenericRole('textbox', textbox),
        'dropdown': GenericRole('dropdown', dropdown),
    }

    # noinspection SpellCheckingInspection
    def merge_domaindata(self, *args, **kwargs) -> None:
        pass

    # noinspection SpellCheckingInspection
    def resolve_any_xref(self, *args, **kwargs) -> List[Tuple[str, Node]]:
        pass


def setup(app: Sphinx):
    app.add_domain(GUIDomain)
    app.add_stylesheet('style/gui.css')
    app.add_node(button,
                 html=(visit_button_html, depart_button_html))
    app.add_node(text,
                 html=(visit_text_html, depart_text_html))
    app.add_node(radio,
                 html=(visit_radio_html, depart_radio_html))
    app.add_node(radio_selected,
                 html=(visit_radio_selected_html, depart_radio_selected_html))
    app.add_node(checkbox,
                 html=(visit_checkbox_html, depart_checkbox_html))
    app.add_node(checkbox_selected,
                 html=(visit_checkbox_selected_html,
                       depart_checkbox_selected_html))
    app.add_node(checkbox_indeterminate,
                 html=(visit_checkbox_indeterminate_html,
                       depart_checkbox_indeterminate_html))
    app.add_node(textbox,
                 html=(visit_textbox_html, depart_textbox_html))
    app.add_node(dropdown,
                 html=(visit_dropdown_html, depart_dropdown_html))
