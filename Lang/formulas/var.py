from typing import *

from Lang.text.text import _text as text

from Lang.html.base_tag import BaseTag

from Lang.formulas.mathml.html.mi import mi

from Lang.formulas.base_var import BaseVar

class Var(BaseVar):
	def __init__(self, name: Any) -> None:
		self._data = name

	def compute(self, **kwargs):
		out = kwargs.get(self._data)
		if(out is None):
			raise ValueError(f"Missing variable: \'{self._data}\'")
		
		return out
	
	def render(self) -> BaseTag:
		return mi(text(str(self._data)))