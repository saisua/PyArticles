from itertools import chain

from Lang.plugin import Plugin
from Lang.glossary.base_glossary_entry import BaseGlossaryEntry

from Lang.html.text_tag import TextTag

from Lang.html.h import h
from Lang.html.b import b
from Lang.html.div import div
from Lang.style.new_page import new_page
from Lang.text.text import _text as text

from Lang.lists.unordered import unordered_list

from Lang.defaults import DEFAULT_GLOSSARY_REF_PREFIX

from Lang.compatibility import *


class BaseGlossary(Plugin):
	_entries: Dict[str, BaseGlossaryEntry]

	def __init__(self) -> None:
		self._entries = dict()

	def __repr__(self) -> str:
		return f"<BaseGlossary entries=[{', '.join(self._entries.keys())}]>"

	def __call__(self, name: str) -> Optional[BaseGlossaryEntry]:
		return self._entries.get(name)
	
	def add(self, name: str, description: str=None, *args: Any, **kwargs: Any) -> BaseGlossaryEntry:
		entry = BaseGlossaryEntry(name=name, description=description)

		self._entries[name] = entry

		return entry
	
	async def setup(self, output_path, output_fname, doc: "Document") -> None:
		self._is_plugin_setup = True	

	async def clear(self) -> None:
		self._entries.clear()

	async def render(self, document: 'document', mode: str | int=None) -> [TextTag, TextTag]:
		if(not len(self._entries)):
			return
		
		return [
			new_page(),
			div([
				h(1, text(document._lang_data['GLOSSARY'])),
				unordered_list([
					div([
						b(
							text(f"{entry.name}:"),
							id=f"{DEFAULT_GLOSSARY_REF_PREFIX}{entry.name}"
						),
						text(f" {entry.description}\n\n")
					])
					for entry in self._entries.values()
				]),
			])
		]
