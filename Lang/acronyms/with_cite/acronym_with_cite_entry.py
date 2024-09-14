from Lang.acronyms.base_acronym_entry import BaseAcronymEntry
from Lang.html.span import span
from Lang.html.a import a
from Lang.text.text import _text

from Lang.compatibility import *

class AcronymWithCiteEntry(BaseAcronymEntry):
	def __call__(self, doc: 'document'=None, mode: str | int=None) -> Any:
		self.counter += 1
		if(self.counter == 1):
			self._registry._used.add(self.short)

			cite = self._registry._citations.cite(self.short)

			return span([
				a(_text(f"{self.long} ({self.short})"), href=self.reference), 
				cite
			])
		return a(_text(self.short), href=self.reference)
	
	def __repr__(self) -> str:
		data = []
		if(self.short):
			data.append(f"short={self.short!r}")
		if(self.long):
			if(isinstance(self.long, str) and len(self.long) > 15):
				data.append(f"long={self.long[:15]}...")
			else:
				data.append(f"long={self.long!r}")
		return f"<AcronymWithCiteEntry{' ' if len(data) > 0 else ''}{' '.join(data)}>"
	
	
	def __str__(self) -> str:
		self.counter += 1
		if(self.counter == 1):
			self._registry._used.add(self.short)

			return f"{self.long} ({self.short})"
		return self.short
	
	@property
	def plural(self):
		return self._plural_wc_cls(self)

	class _plural_wc_cls(BaseAcronymEntry._plural_cls):
		def __call__(self, doc: 'document'=None, mode: str | int=None) -> Any:
			self.counter += 1
			if(self.counter == 1):
				self._bacr._registry._used.add(self._bacr.short)
				
				cite = self._registry._citations.cite(self.short)

				return span([
					a(_text(f"{self.long_plural or self.long} ({self.short_plural})"), href=self.reference),
					cite,
				])
			return a(_text(self.short_plural), href=self.reference)
		
		def __str__(self) -> str:
			self.counter += 1
			if(self.counter == 1):
				self._bacr._registry._used.add(self._bacr.short)

				return f"{self.long_plural or self.long} ({self.short_plural})"
			return self.short_plural
