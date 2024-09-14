from Lang.html.base_tag import _OpenBaseTag, BaseTag, Block
from Lang.html.h import h
from Lang.text.text import _text
from Lang.style.new_page import new_page

from Lang.id import ABSTRACT_ID

from Lang.compatibility import *

class abstract(BaseTag):
	content: Tuple[Block]

	_called: bool = False

	def __init__(self, *next_blocks: Block, **kwargs) -> None:
		self.content = next_blocks

		style = kwargs.get('style', dict())
		if('align' not in style):
			style['align'] = 'justify'

			kwargs['style'] = style

		super().__init__('div', block_id=ABSTRACT_ID, **kwargs)
	

	def __repr__(self) -> str:
		"""
		Shows information about the useful attributes of the object when printed
		Any attribute with length is only shown when length > 0
		The id is not shown
		For strings, keep up to 15 characters max, and if the string is longer than that, add an ellipsis
		"""
		short_content: str
		if(len(self.content) > 15):
			short_content = f"{self.content[:15]}..."
		else:
			short_content = self.content

		return f"<abstract content={short_content!r}>"

	def __call__(self, document: 'Document', *args: Any, mode: str | int=None, **kwargs: Any) -> _OpenBaseTag:
		if (not self._called):
			self._called = True

			content = list(self.content)
			# Update all plain strings with _text with the document's replacements
			for block_n, block in enumerate(content):
				if (isinstance(block, str)):
					content[block_n] = _text(block, document._replacements)

			self._next.extend([
				h(2, document.keywords.ABSTRACT).center(),
				*content
			])

		return [
			new_page(),
			super().__call__(document, *args, **kwargs),
		]
