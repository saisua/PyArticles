import wikipedia

import re

from Lang.glossary.base_glossary import BaseGlossary

from Lang.glossary.base_glossary_entry import BaseGlossaryEntry

from Lang.compatibility import *

wiki_ref_pattern = re.compile(r'\[\d+\]')

class WikipediaGlossary(BaseGlossary):
	def __init__(self, language: str=None) -> None:
		if(language is not None):
			wikipedia.set_lang(language)

		super().__init__()
	
	def add(self, name: str, description: str=None, *args: Any, search: str=None, **kwargs: Any) -> BaseGlossaryEntry:
		if(description is None):
			if(search is None):
				search = name
			try:
				description = wiki_ref_pattern.sub(
					'',
					str(wikipedia.summary(search))
				)
			except Exception as err:
				description = "[WIKIPEDIA GLOSSARY FAILED DUE TO NUMBER OF REQUESTS]"
				print(f"[-] WikipediaGlossary: {err}")

		entry = BaseGlossaryEntry(name=name, description=description)

		self._entries[name] = entry

		return entry
