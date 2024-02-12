from typing import Any
import wikipedia

import re

from Lang.glossary.base_glossary import BaseGlossary

from Lang.glossary.base_glossary_entry import BaseGlossaryEntry

wiki_ref_pattern = re.compile(r'\[\d+\]')

class WikipediaGlossary(BaseGlossary):
	def __init__(self, language: str=None) -> None:
		if(language is not None):
			wikipedia.set_lang(language)

		super().__init__()
	
	def add(self, name: str, description: str=None, *args: Any, **kwargs: Any) -> BaseGlossaryEntry:
		if(description is None):
			try:
				description = wiki_ref_pattern.sub(
					'',
					str(wikipedia.summary(name))
				)
			except Exception as err:
				print(f"[-] WikipediaGlossary: {err}")

		entry = BaseGlossaryEntry(name=name, description=description)

		self._entries[name] = entry

		return entry