from typing import *

from Lang.text.text import _text as text

from Lang.html.base_tag import BaseTag
from Lang.html.a import a

from Lang.formulas.mathml.html.mi import mi

from Lang.formulas.base_var import BaseVar

from Lang.compatibility import *

class Function(BaseVar):
	_function: Callable[[List[Any]], Any]
	_arguments: List[BaseVar]

	def __init__(self, name: Any, function: Callable[[List[Any]], Any]=None) -> None:
		self._data = name
		self._function = function
		self._arguments = []

	def __repr__(self) -> str:
		return f"<Function {self._function}({', '.join(self._arguments)})>"

	def __call__(self, *args: Union[str, BaseVar]) -> Self:
		self._arguments = args

		return self

	def compute(self, **kwargs):
		return self._function([
			computed_arg.compute(**kwargs)
			for arg in self._arguments
		])
	
	def render(self) -> List[Union[BaseTag]]:
		return [
			f"{self._data}(",
			*(
				arg.render()
				for arg in self._arguments
			),
			')',
		]
