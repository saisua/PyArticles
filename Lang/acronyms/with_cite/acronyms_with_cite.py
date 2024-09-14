from Lang.acronyms.base_acronyms import BaseAcronyms, DelayedAcronyms
from Lang.acronyms.with_cite.acronym_with_cite_entry import AcronymWithCiteEntry

from Lang.citations.base_citations import Citations

from Lang.compatibility import *

class AcronymsWithCite(BaseAcronyms):
	_citations: Citations

	def __init__(self, citations: Citations) -> None:
		self._citations = citations

		super().__init__()

	def __repr__(self) -> str:
		return f"<AcronymsWithCite citations={self._citations!r}>"

	def add(self, short: str, long: str=None, *, short_plural: str=None, long_plural: str=None) -> AcronymWithCiteEntry:
		entry = AcronymWithCiteEntry(
			registry=self,
			short=short, 
			long=long, 
			short_plural=short_plural, 
			long_plural=long_plural
		)

		self._entries[short] = entry

		return entry
