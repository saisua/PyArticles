from itertools import chain
from typing import Coroutine

from Lang.plugin import Plugin
from Lang.acronyms.base_acronym_entry import BaseAcronymEntry
from Lang.core.block import Block

from Lang.html.text_tag import TextTag

from Lang.html.div import div
from Lang.html.b import b
from Lang.html.h import h
from Lang.text.text import _text as text

from Lang.style.new_page import new_page

from Lang.lists.unordered import unordered_list

from Lang.defaults import DEFAULT_ACRONYM_REF_PREFIX

from Lang.compatibility import *

class DelayedAcronyms(TextTag):
	_acro: 'BaseAcronyms'
	def __init__(self, acro: 'BaseAcronyms', *args, next_blocks: List[Block] | None = None, **kwargs) -> None:
		self._acro = acro

		super().__init__('div', *args, next_blocks=next_blocks, **kwargs)

	def __repr__(self) -> str:
		return f"<DelayedAcronyms acronyms={self._acro!r}>"

	def __call__(self, document: 'Document', mode: str | int=None, *args: Any, **kwargs: Any) -> None:
		if(not len(self._acro._used)):
			return

		self._next.extend([
			new_page(),
			h(1, text(document._lang_data['ACRONYMS'])),
			unordered_list(list((
				div([
					b(
						text(f"{entry.short}{' / ' + entry.short_plural if entry.short_plural else ''}:"),
						id=f"{DEFAULT_ACRONYM_REF_PREFIX}{entry.short}"
					),
					text(f" {entry.long}{' / ' + entry.long_plural if entry.long_plural else ''}\n")
				])
				for entry_name, entry in self._acro._entries.items()
				if entry_name in self._acro._used
			)))
		])

class BaseAcronyms(Plugin):
	_entries = Dict[str, BaseAcronymEntry]
	_used = Set[str]

	def __init__(self) -> None:
		self._entries = dict()
		self._used = set()

	def __repr__(self) -> str:
		return f"<BaseAcronyms _entries=[{', '.join(self._entries.keys())!r}]>"

	async def setup(self, output_path, output_fname, doc: "Document") -> None:
		self._is_plugin_setup = True	

	async def clear(self) -> None:
		self._used.clear()

		entry: BaseAcronymEntry
		for entry in self._entries.values():
			entry.clear()
	
	async def render(self, document: 'document', mode: str | int=None) -> DelayedAcronyms:
		return DelayedAcronyms(self)

	def add(self, short: str, long: str=None, *, short_plural: str=None, long_plural: str=None) -> BaseAcronymEntry:
		entry = BaseAcronymEntry(
			registry=self,
			short=short, 
			long=long, 
			short_plural=short_plural, 
			long_plural=long_plural
		)

		self._entries[short] = entry

		return entry
	
	def __call__(self, name: str, *args: Any, **kwds: Any) -> Optional[BaseAcronymEntry]:
		return self._entries.get(name)

