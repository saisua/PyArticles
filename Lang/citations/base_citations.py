import aiofiles
import os

import pybtex.database
from pybtex.style.formatting.unsrt import Style

from Lang.plugin import Plugin
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

from Lang.compatibility import *


class DelayedCitations(TextTag):
	_citations: 'Citations'
	def __init__(self, citations: 'Citations', *args, next_blocks: List[Block] | None = None, **kwargs) -> None:
		self._citations = citations

		super().__init__('div', *args, next_blocks=next_blocks, **kwargs)

	def __repr__(self) -> str:
		return f"<DelayedCitations citations={self._citations}>"

	def __call__(self, document: 'Document', *args: Any, mode: str | int=None, **kwargs: Any) -> None:
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


class Citations(Plugin):
	_data: Optional[pybtex.database.BibliographyData]
	_style: Style
	_cited: List[str]

	_filename: str
	_format: str

	def __init__(self, filename: str='bibliography.bib', format: str='bibtex', *args, **kwargs) -> None:
		self._style = Style(*args, **kwargs)
		self._data = None
		self._cited = list()

		self._filename = filename
		self._format = format

	def __repr__(self) -> str:
		return f"<Citations _cited={self._cited!r}>"

	def __contains__(self, entry: str) -> bool:
		return entry in self._data.entries

	async def setup(self, output_path, output_fname, doc: 'Document'):
		if (not self._is_plugin_setup):
			await self.reload(os.path.join(output_path, self._filename), self._format)

			self._is_plugin_setup = True
		
	async def reload(self, filename: str, format: str='bibtex'):
		bib_text: str
		async with aiofiles.open(filename, 'r') as f:
			bib_text = await f.read()

		self._data = pybtex.database.parse_string(bib_text, format) or dict()

	async def clear(self) -> None:
		self._cited.clear()

	async def render(self, document: 'document', mode: str | int=None) -> DelayedCitations:
		return DelayedCitations(self)

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
	
	@property
	def loaded(self) -> bool:
		return self._data is not None
