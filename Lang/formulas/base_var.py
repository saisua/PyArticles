from typing import *

from Lang.core.block import Block


class BaseVar:
	_data: Block | str

	def __truediv__(self, data: Block | str | int) -> 'Division':
		from Lang.formulas.mathml.division import Division
		return Division(self, data)

	def __abs__(self) -> 'Abs':
		from Lang.formulas.mathml.abs import Abs
		return Abs(self)