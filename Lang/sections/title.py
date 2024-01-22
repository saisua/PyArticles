from typing import *
from typing import Any

from Lang.html.base_tag import _OpenBaseTag, BaseTag, Block
from Lang.html.h import h
from Lang.text.text import _text as text
from Lang.style.new_page import new_page

from Lang.id import TITLE_ID


class title(BaseTag):
	title: str
	subtitle: str
	authors: str

	def __init__(self, title: str=None, subtitle: str=None, authors: str=None, *args, next_blocks: List[Block] | None = None, **kwargs) -> None:
		self.title = title
		self.subtitle = subtitle
		self.authors = authors

		super().__init__('div', *args, block_id=TITLE_ID, next_blocks=next_blocks, **kwargs)

		new_page(self)

	def __call__(self, document: 'Document', *args: Any, **kwargs: Any) -> _OpenBaseTag:
		if(self.title):
			if(isinstance(self.title, str)):
				self._next.append(
					h(1, text(self.title), **{'class': 'title'})
				)
			else:
				self._next.append(
					self.title
				)
		if(self.subtitle):
			if(isinstance(self.title, str)):
				self._next.append(
					h(2, text(self.subtitle), **{'class': 'subtitle'})
				)
			else:
				self._next.append(
					self.subtitle
				)
		if(self.authors):
			if(isinstance(self.authors, str)):
				self._next.append(
					h(3, text(self.authors), **{'class': 'authors'})
				)
			else:
				self._next.append(
					self.authors
				)
		
		return [
			new_page(),
			super().__call__(document, *args, **kwargs),
		]