from Lang.core.block import Block

from Lang.formulas.base_var import BaseVar
from Lang.formulas.value import Value

from Lang.formulas.mathml.html.msup import msup

from Lang.text.text import _text as text

from Lang.html.base_tag import BaseTag

from Lang.compatibility import *

class Pow(BaseVar):
	def __init__(self, d0: BaseVar | str | int, d1: BaseVar | str | int, ) -> None:
		if(not isinstance(d0, BaseVar)):
			d0 = Value(d0)
		if(not isinstance(d1, BaseVar)):
			d1 = Value(d1)

		self._data = (d0, d1)

	def __repr__(self) -> str:
		return f"<Pow {self._data[0]!r} ^ {self._data[1]!r}>"

	def compute(self, **kwargs):
		d0 = self._data[0]
		if(isinstance(d0, BaseVar)):
			d0 = d0.compute(**kwargs)

		d1 = self._data[1]
		if(isinstance(d1, BaseVar)):
			d1 = d1.compute(**kwargs)

		return d0 ** d1
 #
	# def _apply_d1_style(self, d1: Union[Block, List[Block], Tuple[Block]]) -> None:
	# 	if(not isinstance(d1, (list, tuple))):
	# 		d1 = [d1]
 #
	# 	for sub_d1 in d1:
	# 		font_size(sub_d1, 'smaller')
	# 		vertical_align(sub_d1, 'super')
	
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
		return msup([
			d0,
			d1,
		])
