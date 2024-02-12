from typing import *

from Lang.core.block import Block


class BaseVar:
	_data: Block | str

	def __truediv__(self, data: Block | str | int) -> 'Division':
		from Lang.formulas.mathml.division import Division
		return Division(self, data)

	def __rtruediv__(self, data: Block | str | int) -> 'Division':
		from Lang.formulas.mathml.division import Division
		return Division(data, self)

	def __abs__(self) -> 'Abs':
		from Lang.formulas.mathml.abs import Abs
		return Abs(self)

	def __add__(self, data: Block | str | int) -> 'Add':
		from Lang.formulas.mathml.add import Add
		return Add(self, data)

	def __radd__(self, data: Block | str | int) -> 'Add':
		from Lang.formulas.mathml.add import Add
		return Add(data, self)

	def __pow__(self, data: Block | str | int) -> 'Pow':
		from Lang.formulas.mathml.pow import Pow
		return Pow(self, data)

	def __rpow__(self, data: Block | str | int) -> 'Pow':
		from Lang.formulas.mathml.pow import Pow
		return Pow(data, self)

	def __neg__(self) -> 'Neg':
		from Lang.formulas.mathml.neg import Neg
		return Neg(self)

	def compute(self):
		return self._data

	def render(self):
		return str(self._data)
