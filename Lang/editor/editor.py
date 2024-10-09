import os

from Lang.compatibility import Any
from Lang.html.base_tag import _OpenBaseTag, BaseTag
from Lang.html.div import div
from Lang.html.script import script

from .toggle import Toggle
from .dropdown import Dropdown
from .textarea import TextArea

from Lang.compatibility import *

editor_js_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'editor.js')
with open(editor_js_path, 'r') as f:
    editor_js = f.read()

class Editor(BaseTag):
    _toggle: Toggle
    _dropdown: Dropdown

    def __init__(self, *args, **kwargs) -> None:
        self._toggle = Toggle(*args, **kwargs)
        self._dropdown = Dropdown(*args, **kwargs)
        self._textarea = TextArea(*args, **kwargs)

        super().__init__('div', *args, **kwargs)

        self._next.extend((
            self._toggle,
            self._dropdown,
            self._textarea,
        ))

    def __repr__(self) -> str:
        return "<Editor>"

    def __call__(self, document: 'Document', *args: Any, mode: str | int = None, **kwargs: Any) -> _OpenBaseTag:
        self._next.extend((
            div(id="document-path", path=document.path.rstrip('/')+'/'),
            script(editor_js),
        ))

        return super().__call__(document, *args, mode=mode, **kwargs)