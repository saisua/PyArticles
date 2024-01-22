from typing import *

import re

from Lang.html.base_tag import Block
from Lang.html.text_tag import TextTag

from Lang.html.span import span

from Lang.id import TEXT_ID

from Lang.style.utils.enable_newlines_text import enable_newlines_text

space_cleanup_re: re.Pattern = re.compile(r"([ \t]+|\n(?!\n))")
nl_cleanup_re: re.Pattern = re.compile(r"\n+")

class _text(Block):
	text: str

	_format_args: Tuple[str, ...]
	_format_kwargs: Dict[str, str]

	def __init__(self, text: str, *args, next_blocks: List[Block] | None = None, **kwargs) -> None:
		self.text = nl_cleanup_re.sub(
			'\n',
			space_cleanup_re.sub(' ', 
				text
		)	)

		self._format_args = tuple()
		self._format_kwargs = dict()

		super().__init__(*args, block_id=TEXT_ID, next_blocks=next_blocks, **kwargs)

	def __call__(self, document: 'Document', *args: Any, **kwargs: Any) -> None:
		document.text(self.render())

	def render(self) -> str:
		return self._formatted_text(str(self.text))

	def _formatted_text(self, text: str) -> str:
		return text.format(*self._format_args, **self._format_kwargs)

	def format(self, *args, **kwargs):
		self._format_args = args
		self._format_kwargs = kwargs
	
def text(text: str, *args, next_blocks: List[Block] | None = None, format: Dict=None, tag: Block=span, **kwargs) -> TextTag:
	text = _text(text)

	if(format is not None):
		text.format(**format)

	if(next_blocks is None):
		next_blocks = text
	elif(isinstance(next_blocks, list)):
		next_blocks.insert(0, text)
	elif(isinstance(next_blocks, tuple)):
		next_blocks = [text, *next_blocks]
	else:
		next_blocks = [text, next_blocks]
	
	tag = tag(next_blocks, *args, **kwargs)
	enable_newlines_text(tag)

	return tag