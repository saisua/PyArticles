from Lang.formulas.base_var import BaseVar
from Lang.formulas.value import Value

from Lang.formulas.mathml.html.mfrac import mfrac
from Lang.formulas.mathml.html.mn import mn
from Lang.formulas.mathml.html.mo import mo

from Lang.html.div import div

from Lang.text.text import _text as text

from Lang.html.base_tag import BaseTag

from Lang.symbols import ABSOLUTE_SYMBOL

from Lang.compatibility import *

class Abs(BaseVar):
	def __init__(self, d0: BaseVar | str | int) -> None:
		if(not isinstance(d0, BaseVar)):
			d0 = Value(d0)

		self._data = d0

	def __repr__(self) -> str:
		return f"<Abs {self._data!r}>"

	def compute(self, **kwargs):
		d0 = self._data
		if(isinstance(self._data, BaseVar)):
			d0 = d0.compute(**kwargs)

		return abs(d0)
	
	def render(self) -> BaseTag:
		d0 = self._data
		if(isinstance(d0, BaseVar)):
			d0 = d0.render()
		else:
			d0 = text(str(d0))

		# Idk why, but there can't be a 'div' returned here
		return [
			mo(text(ABSOLUTE_SYMBOL)),
			d0,
			mo(text(ABSOLUTE_SYMBOL)),
		]
