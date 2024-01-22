from typing import Any

from Lang.core.block import Block

from Lang.html.a import a

from Lang.text.text import _text

from Lang.id import ACRONYM_ID

class BaseAcronymEntry(Block):
	_registry: 'BaseAcronyms'

	short: str
	short_plural: str
	long: str
	long_plural: str

	counter: int

	def __init__(self, registry: 'BaseAcronyms', short: str, long: str=None, *, short_plural: str=None, long_plural: str=None) -> None:
		self._registry = registry

		self.short = short
		self.long = long

		self.short_plural = short_plural
		self.long_plural = long_plural

		self.counter = 0

		super().__init__(block_id=ACRONYM_ID)

	def clear(self) -> None:
		self.counter = 0

	def __str__(self) -> str:
		self.counter += 1
		if(self.long and self.counter == 1):
			self._registry._used.add(self.short)

			return a(_text(f"{self.long} ({self.short})"), href=self.reference)
		return a(_text(self.short), href=self.reference)
	
	@property
	def reference(self):
		return f"#acro.{self.short}"

	@property
	def plural(self):
		return self._plural_cls(self)

	class _plural_cls:
		_bacr: 'BaseAcronymEntry'=None

		def __init__(self, bacr: 'BaseAcronymEntry') -> None:
			self._bacr = bacr
		
		def __str__(self) -> str:
			self.counter += 1
			if(self.long_plural and self.counter == 1):
				self._bacr._registry._used.add(self._bacr.short)
				
				return a(_text(f"{self.long_plural} ({self.short_plural})"), href=self.reference)
			return a(_text(self.short_plural), href=self.reference)

		def __getattr__(self, __name: str) -> Any:
			if(__name == '_bacr'):
				return self.__dict__['_bacr']
			
			return self.__dict__['_bacr'].__getattribute__(__name)
		
		def __setattr__(self, __name: str, value: Any) -> Any:
			if(__name == '_bacr'):
				self.__dict__['_bacr'] = value
			
			self.__dict__['_bacr'].__setattr__(__name, value)
