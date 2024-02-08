from typing import *

import aiofiles

import pybtex.database
from pybtex.style.formatting.unsrt import Style

from Lang.core.block import Block

from Lang.html.base_tag import BaseTag
from Lang.html.text_tag import TextTag

from Lang.html.div import div
from Lang.html.span import span
from Lang.html.h import h
from Lang.html.a import a
from Lang.html.br import br
from Lang.style.new_page import new_page
from Lang.text.text import _text as text

from Lang.defaults import DEFAULT_CITATION_REF_PREFIX


class DelayedCitations(TextTag):
	_citations: 'Citations'
	def __init__(self, citations: 'Citations', *args, next_blocks: List[Block] | None = None, **kwargs) -> None:
		self._citations = citations

		super().__init__('div', *args, next_blocks=next_blocks, **kwargs)

	def __call__(self, document: 'Document', *args: Any, **kwargs: Any) -> None:
		if(not len(self._citations._cited)):
			return

		entries = sorted((
				entry
				for entry in self._citations._style.format_bibliography(self._citations._data)
				if entry.key in self._citations._cited
			),
			key=lambda entry: self._citations._cited.index(entry.key)
		)

		self._next.extend([
			new_page(),
			h(1, text(document._lang_data['BIBLIOGRAPHY'])),
			*(
				span([
						text(f"[{self._citations._cited.index(entry.key)}] {entry.text.render_as('text')}"),
						br(),
					],
					id=f"{DEFAULT_CITATION_REF_PREFIX}{entry.key}"
				)
				for entry in entries
			)
		])


class Citations:
	_data: Optional[pybtex.database.BibliographyData]
	_style: Style
	_cited: List[str]

	def __init__(self, *args, **kwargs) -> None:
		self._style = Style(*args, **kwargs)
		self._data = None
		self._cited = list()

	def __contains__(self, entry: str) -> bool:
		return entry in self._data.entries

	async def load_bibliography(self, filename: str, format: str='bibtex'):
		bib_text: str
		async with aiofiles.open(filename, 'r') as f:
			bib_text = await f.read()

		self._data = pybtex.database.parse_string(bib_text, format)

	def clear(self) -> None:
		self._cited.clear()

	def cite(self, cite: str, text_after: str='') -> Optional[TextTag]:
		entry = self._data.entries.get(cite)

		if(entry is None):
			return
		
		try:
			entry_num = self._cited.index(entry.key)
		except ValueError:
			entry_num = len(self._cited)
			self._cited.append(entry.key)
		
		return a(
			text(f"[{entry_num}]{text_after}"),
			href=f"#{DEFAULT_CITATION_REF_PREFIX}{entry.key}"
		)
	
	__call__ = cite

	def render(self, document: 'document') -> DelayedCitations:
		return DelayedCitations(self)
	
	@property
	def loaded(self) -> bool:
		return self._data is not None
