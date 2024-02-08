from typing import *

from Lang.core.block import Block, OpenBlock
from Lang.html.base_tag import BaseTag

from Lang.html.div import div
from Lang.html.h import h
from Lang.html.a import a
from Lang.text.text import _text as text

from Lang.style.utils.margin_left import margin_left

from Lang.defaults import DEFAULT_REFERENCE_KEY

class DelayedIndex(BaseTag):
	_index: 'Index'
	def __init__(self, index: 'Index', *args, block_id: int = None, next_blocks: List[Block] | None = None, **kwargs) -> None:
		self._index = index

		super().__init__('div', *args, block_id=block_id, next_blocks=next_blocks, **kwargs)

	def __call__(self, document: 'Document', *args: Any, **kwargs: Any) -> None:
		args, kwargs = self._merge_args_kwargs(args, kwargs, style_to_str=False)

		self._next.append(
			margin_left(
				div([
					h(1, text(document._lang_data["INDEX"])),
					*(
						margin_left(
							div(a(
								h(
									min(6, section_number.count('.') + 2), 
									text(f"{section_number}{self._index._sep}{section_name}"),
								),
								href=f"#{section_name}",
							)),
							f"{min(6, section_number.count('.'))*self._index._bleeding}%"
						)
						for section_number, section_name in self._index._section_names.items()
					)],
					*args, **kwargs
				),
				'5%'
		)	)

class Index:
	_section_names: Dict[str, str]
	_section: List[int]

	_bleeding: float
	_sep: str

	_kwargs: dict

	def __init__(self, *args, next_blocks: List[Block] | None = None, bleeding: float=1.5, sep: str='. ', **kwargs) -> None:
		self._section = [0]
		self._section_names = {}

		self._bleeding = 1.5
		self._sep = sep

		self._kwargs = kwargs

	def clear(self) -> None:
		self._section_names.clear()
		self._section.clear()
		self._section.append(0)

	def __call__(self, section_name: str, *args: Any, bleeding: float=None, **kwargs: Any) -> str:
		self._section[-1] += 1

		section_number = '.'.join(map(str, self._section))

		self._section_names[section_number] = section_name

		_kwargs = self._kwargs.copy()
		_kwargs.update(kwargs)

		return margin_left(
			div(h(
				min(6, len(self._section) - 1 or 1), 
				text(f"{section_number}{self._sep}{section_name}"),
				id=_kwargs.get(DEFAULT_REFERENCE_KEY, section_name),
			), *args, **kwargs),
			f"{min(6, len(self._section) - 1)*(bleeding or self._bleeding)}%"
		)

	def __enter__(self, *args, **kwargs) -> Self:
		self._section.append(0)
		return self

	def __exit__(self, *args, **kwargs):
		self._section.pop(-1)

	def render(self, document: 'document') -> Block:
		return DelayedIndex(self)
