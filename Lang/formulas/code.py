from typing import *
import inspect
import re
from math import ceil, log10
from functools import partial

from Lang.html.base_tag import BaseTag

from Lang.html.div import div
from Lang.html.br import br
from Lang.html.tt import tt

from Lang.text.text import _text

from Lang.divider.horizontal_divider import horizontal_divider

from Lang.compatibility import *

class Code:
    _function: Callable
    _name: str
    _doc: str
    _short_doc: str=None

    _head: str
    _render_doc: Optional[str]
    _inputs: Optional[str]
    _outputs: Optional[str]
    _code_lines: list[str]

    _replacements: Dict[str, Any]

    def __init__(self, 
                 function: Callable[[List[Any]], Any],
                 head: str=None,
                 name: str=None,
                 doc: str=None,
                 inputs: str=None,
                 outputs: str=None,
                 code_lines: List[str]=None,
                 
        ) -> None:
        self._function = function

        if(name is None):
            self._name = function.__name__
        else:
            self._name = name
        
        if(doc is None):
            self._doc = function.__doc__.strip()
        else:
            self._doc = doc.strip()
        
        if self._doc is not None:
            self._short_doc = self._doc.split('\n', 1)[0]

        if(head is None):
            self._head = self._parse_head()
        else:
            self._head = head
        
        self._render_doc = self._parse_doc()

        if inputs is None:
            self._inputs = self._parse_inputs(function)
        else:
            self._inputs = inputs
        
        if outputs is None:
            self._outputs = self._parse_outputs(function)
        else:
            self._outputs = outputs
        
        if code_lines is None:
            self._code_lines = self._parse_code(function)
        else:
            self._code_lines = code_lines

    def __call__(self, *args, **kwargs) -> Self:
        return self._function(*args, **kwargs)

    def __repr__(self) -> str:
        return f"<ParsedFunction {self._function}>"
    
    def _parse_head(self) -> str:
        if(self._short_doc is not None):
            return f"{self._name}: {self._short_doc}"
        else:
            return self._name

    def _parse_doc(self) -> Optional[str]:
        if(self._short_doc is None or (
                self._doc is not None and 
                self._doc != self._short_doc
            )   ):
            return self._doc
        else:
            return None

    def _parse_inputs(self, function) -> Optional[str]:
        fn_params = inspect.signature(function).parameters
        fn_type_hints = get_type_hints(function)

        inputs = []
        for name in fn_params.keys():
            hint = fn_type_hints.get(name)

            if(hint is not None):
                type_name = self.format_type(hint)
                inputs.append(f"{type_name} {name}")
            else:
                inputs.append(name)

        if(len(inputs) == 0):
            return
        
        return f"Inputs: {', '.join(inputs)}"

    def _parse_outputs(self, function) -> Optional[str]:
        _type_hints = get_type_hints(function)

        out_type = _type_hints.get('return')
        if(out_type is None):
            return
        
        return f"Output: {self.format_type(out_type)}"

    def _parse_code(self, function) -> List[str]:
        code = inspect.getsource(function)
        # Remove the definition of the function
        code = re.split("\)\s*(\-\>\s*[^:]+)?\:\s*", code, 1)[2]
        # # Remove all comments
        code = re.sub(r"\"\"\".*?\"\"\"", "", code, flags=re.DOTALL)
        code = re.sub(r"#.*", "", code)

        # # Split into lines
        code_lines = code.split('\n')

        # Get the first non-empty line
        non_empty_indices = [
            i
            for i, line in enumerate(code_lines)
            if line.strip() != ""
        ]
        if (len(non_empty_indices) == 0):
            return []

        code_lines = code_lines[non_empty_indices[0] : non_empty_indices[-1] + 1]

        # Get the initial indent
        indent = re.search(r"^\s*", code_lines[0]).group(0)

        # Remove the initial indent
        code_lines = map(lambda x: re.sub(rf"^{indent}", "", x, 1), code_lines)
        # Set tabs to be renderable
        # code_lines = map(lambda x: x.replace("\t", "    "), code_lines)
        code_lines = list(code_lines)

        if (len(code_lines) == 0):
            return []

        # # Add a number to each line
        max_lines_log10 = ceil(log10(len(code_lines)))
        return list((
            f"{n: <{max_lines_log10}} | {line} "
            for n, line in enumerate(code_lines)
        ))

    def render(self) -> List[Union[BaseTag]]:
        return tt([
            horizontal_divider(),
            self._head,
            horizontal_divider(),
            self._render_doc,
            br() if self._render_doc is not None else None,
            self._inputs,
            br(),
            self._outputs,
            br(),
            *map(div, map(partial(_text, apply_formatting=False), self._code_lines)),
            horizontal_divider(),
        ])
    
    @staticmethod
    def format_type(type_) -> str:
        """Maps Python types to readable strings."""
        if type_ is int:
            return "Integer"
        elif type_ is str:
            return "String"
        elif type_ is float:
            return "Float"
        elif type_ is bool:
            return "Boolean"
        elif type(type_) is str:
            return type_
        # Add more mappings as needed
        else:
            return str(type_).replace('typing.', '').title() 