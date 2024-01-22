from typing import Any
import wikipedia

from Lang.glossary.base_glossary import BaseGlossary

from Lang.glossary.base_glossary_entry import BaseGlossaryEntry

class WikipediaGlossary(BaseGlossary):
	def __init__(self, language: str=None) -> None:
		if(language is not None):
			wikipedia.set_lang(language)

		super().__init__()
	
	def add(self, name: str, description: str=None, *args: Any, **kwargs: Any) -> BaseGlossaryEntry:
		if(description is None):
			try:
				description = wikipedia.summary(name)
			except Exception:
				...

		entry = BaseGlossaryEntry(name=name, description=description)

		self._entries[name] = entry

		return entry