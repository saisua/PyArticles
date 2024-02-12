from typing import *

import re

from Lang.html.base_tag import Block
from Lang.html.text_tag import TextTag

from Lang.html.span import span

from Lang.id import TEXT_ID

from Lang.style.utils.enable_newlines_text import enable_newlines_text

lone_nl_cleanup_re: re.Pattern = re.compile(r"([^\n]|^)\n([^\n]|$)")
space_cleanup_re: re.Pattern = re.compile(r"[ \t]+")
nl_cleanup_re: re.Pattern = re.compile(r"\n{2}")

class _text(Block):
	text: str
	replacements: Dict

	_format_args: Tuple[str, ...]
	_format_kwargs: Dict[str, str]

	def __init__(self, text: str, replacements: Dict={}, *args, next_blocks: List[Block] | None = None, **kwargs) -> None:
		self.text = text
		self.replacements = replacements

		self._format_args = tuple()
		self._format_kwargs = dict()

		super().__init__(*args, block_id=TEXT_ID, next_blocks=next_blocks, **kwargs)

	def __call__(self, document: 'Document', *args: Any, **kwargs: Any) -> None:
		rendered_text = self.render()

		if(isinstance(rendered_text, str)):
			document.text(rendered_text)
		elif(isinstance(rendered_text, (list, tuple))):
			new_next = []
			for sub_block in rendered_text:
				if(isinstance(sub_block, str)):
					new_next.append(_text(sub_block))
				else:
					new_next.append(sub_block)

			self._next = [*new_next, *self._next]

	def render(self):
		return self._formatted_text(self.text)

	def _formatted_text(self, text: str) -> str:
		text = self._cleanup_format(text)
		text = text.format(*self._format_args, **self._format_kwargs)
		if(len(self.replacements)):
			text = self._replacement_format(text)
		return text

	def _cleanup_format(self, text: str) -> str:
		return nl_cleanup_re.sub(
			'\n',
			lone_nl_cleanup_re.sub(
				'\g<1>\g<2>',
			space_cleanup_re.sub(
				' ',
				text
		)))

	def _replacement_format(self, text: str) -> Union[str, list]:
		secondary_queue = []
		text_queue = [text]

		replacements = dict(reversed(sorted(
			self.replacements.items(),
			key=lambda tup: len(tup[0])
		)))

		for token, replacement in replacements.items():
			for text in text_queue:
				if(not isinstance(text, str)):
					secondary_queue.append(text)
					continue

				split_text = text.split(token)
				for n, split in enumerate(split_text):
					if(n):
						secondary_queue.append(replacement)
					secondary_queue.append(split)

			text_queue, secondary_queue = secondary_queue, text_queue
			secondary_queue.clear()

		if(len(text_queue) == 1):
			return text_queue[0]
		return text_queue

	def format(self, *args, **kwargs):
		self._format_args = args
		self._format_kwargs = kwargs
	
def text(text: str, replacements: Dict={}, *args, next_blocks: List[Block] | None = None, format: Dict=None, tag: Block=span, **kwargs) -> TextTag:
	text = _text(text, replacements)

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
