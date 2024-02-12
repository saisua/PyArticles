from typing import *

from Lang.formulas.base_var import BaseVar

from Lang.formulas.mathml.html.math import math

class Formula:
	_data: BaseVar

	def __init__(self, var: BaseVar):
		self._data = var

	def compute(self, **kwargs):
		return self._data.compute(**kwargs)

	def render(self) -> BaseVar:
		return math(self._data.render())
