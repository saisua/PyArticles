from typing import *

from Lang.text.text import _text as text

from Lang.html.base_tag import BaseTag

from Lang.formulas.mathml.html.mi import mi

from Lang.formulas.base_var import BaseVar

class Var(BaseVar):
	_value: Any

	def __init__(self, name: Any, value: Any=None) -> None:
		self._data = name
		self._value = value

	def compute(self, **kwargs):
		out = kwargs.get(self._data, self._value)
		if(out is None):
			raise ValueError(f"Missing variable: \'{self._data}\'")
		
		return out
	
	def render(self) -> BaseTag:
		return mi(text(str(self._data)))
