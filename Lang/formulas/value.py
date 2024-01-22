from typing import *

from Lang.text.text import _text as text

from Lang.html.base_tag import BaseTag

from Lang.formulas.mathml.html.mn import mn

from Lang.formulas.base_var import BaseVar

class Value(BaseVar):
	def __init__(self, value: Any) -> None:
		self._data = value

	def compute(self, **kwargs):
		return self._data
	
	def render(self) -> BaseTag:
		return mn(text(str(self._data)))