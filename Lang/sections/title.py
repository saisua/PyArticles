from Lang.html.base_tag import _OpenBaseTag, BaseTag, Block
from Lang.html.h import h
from Lang.text.text import _text as text
from Lang.style.new_page import new_page

from Lang.id import TITLE_ID

from Lang.compatibility import *

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

	def __repr__(self) -> str:
		repr = ['<title']

		if(self.title is not None):
			if(isinstance(self.title, str)):
				if(len(self.title) > 10):
					repr.append(f" title={self.title[:10]}...")
				else:
					repr.append(f" title={self.title}")
			else:
				repr.append(f" title={self.title.__repr__()}")

		if(self.subtitle is not None):
			if(isinstance(self.subtitle, str)):
				if(len(self.subtitle) > 10):
					repr.append(f" subtitle={self.subtitle[:10]}...")
				else:
					repr.append(f" subtitle={self.subtitle}")
			else:
				repr.append(f" subtitle={self.subtitle.__repr__()}")

		if(self.authors is not None):
			if(isinstance(self.authors, str)):
				if(len(self.authors) > 10):
					repr.append(f" authors={self.authors[:10]}...")
				else:
					repr.append(f" authors={self.authors}")
			else:
				repr.append(f" authors={self.authors.__repr__()}")

		repr.append('>')

		return ''.join(repr)

	def __call__(self, document: 'Document', *args: Any, mode: str | int=None, **kwargs: Any) -> _OpenBaseTag:
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
