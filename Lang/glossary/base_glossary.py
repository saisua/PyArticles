from typing import *

from itertools import chain

from Lang.glossary.base_glossary_entry import BaseGlossaryEntry

from Lang.html.text_tag import TextTag

from Lang.html.h import h
from Lang.html.b import b
from Lang.html.div import div
from Lang.style.new_page import new_page
from Lang.text.text import _text as text

from Lang.lists.unordered import unordered_list

from Lang.defaults import DEFAULT_GLOSSARY_REF_PREFIX

class BaseGlossary:
	_entries: Dict[str, BaseGlossaryEntry]

	def __init__(self) -> None:
		self._entries = dict()

	def add(self, name: str, description: str=None, *args: Any, **kwargs: Any) -> BaseGlossaryEntry:
		entry = BaseGlossaryEntry(name=name, description=description)

		self._entries[name] = entry

		return entry

	def __call__(self, name: str) -> Optional[BaseGlossaryEntry]:
		return self._entries.get(name)
	
	def render(self, document: 'document') -> [TextTag, TextTag]:
		if(not len(self._entries)):
			return
		
		return [
			new_page(),
			div([
				h(1, text(document._lang_data['GLOSSARY'])),
				unordered_list([
					div([
						b(
							text(f"{entry.name}:\n"),
							id=f"{DEFAULT_GLOSSARY_REF_PREFIX}{entry.name}"
						),
						text(f"{entry.description}\n\n")
					])
					for entry in self._entries.values()
				]),
			])
		]