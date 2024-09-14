from Lang.core.block import Block

from Lang.formulas.base_var import BaseVar

from Lang.formulas.mathml.html.math import math

from Lang.compatibility import *

class Formula(Block):
	_data: BaseVar

	def __init__(self, var: BaseVar):
		self._data = var

	def __repr__(self) -> str:
		return f"<Formula {self._data!r}>"

	def compute(self, **kwargs):
		return self._data.compute(**kwargs)

	def render(self) -> BaseVar:
		return math(self._data.render())

	def __call__(self) -> BaseVar:
		return self.render()
