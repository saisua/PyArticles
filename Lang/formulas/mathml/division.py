from Lang.formulas.base_var import BaseVar
from Lang.formulas.value import Value

from Lang.formulas.mathml.html.mfrac import mfrac
from Lang.formulas.mathml.html.mrow import mrow
from Lang.formulas.mathml.html.mn import mn

from Lang.html.div import div

from Lang.text.text import _text as text

from Lang.html.base_tag import BaseTag

from Lang.compatibility import *

class Division(BaseVar):
	def __init__(self, d0: BaseVar | str | int, d1: BaseVar | str | int, ) -> None:
		if(not isinstance(d0, BaseVar)):
			d0 = Value(d0)
		if(not isinstance(d1, BaseVar)):
			d1 = Value(d1)

		self._data = (d0, d1)

	def __repr__(self) -> str:
		return f"<Division {self._data[0]!r} / {self._data[1]!r}>"

	def compute(self, **kwargs):
		d0 = self._data[0]
		if(isinstance(d0, BaseVar)):
			d0 = d0.compute(**kwargs)

		d1 = self._data[1]
		if(isinstance(d1, BaseVar)):
			d1 = d1.compute(**kwargs)

		return d0 / d1
	
	def render(self) -> BaseTag:
		d0 = self._data[0]
		if(isinstance(d0, BaseVar)):
			d0 = d0.render()
		else:
			d0 = text(str(d0))

		d1 = self._data[1]
		if(isinstance(d1, BaseVar)):
			d1 = d1.render()
		else:
			d1 = text(str(d1))

		# Idk why, but there can't be a 'div' returned here
		return mfrac([
			mrow(d0),
			mrow(d1),
		])
