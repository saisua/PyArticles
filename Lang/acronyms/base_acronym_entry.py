from Lang.core.block import Block

from Lang.html.a import a

from Lang.text.text import _text

from Lang.id import ACRONYM_ID

from Lang.compatibility import *

class BaseAcronymEntry(Block):
	_registry: 'BaseAcronyms'

	_short: str
	_short_plural: str
	_long: str
	_long_plural: str

	counter: int

	_transformations: List[Callable]

	def __init__(self, registry: 'BaseAcronyms', short: str, long: str=None, *, short_plural: str=None, long_plural: str=None) -> None:
		self._registry = registry

		self._short = short
		self._long = long

		self._short_plural = short_plural
		self._long_plural = long_plural

		self.counter = 0

		self._transformations = []

		super().__init__(block_id=ACRONYM_ID)

	def __repr__(self) -> str:
		data = []

		if(self._short):
			data.append(f"short={self._short!r}")

		if(self._short_plural):
			data.append(f"short_plural={self._short_plural!r}")

		if(self._long):
			if(len(self._long) > 15):
				data.append(f"long={self._long[:15]}...")
			else:
				data.append(f"long={self._long!r}")

		if(self._long_plural):
			if(len(self._long_plural) > 15):
				data.append(f"long_plural={self._long_plural[:15]}...")
			else:
				data.append(f"long_plural={self._long_plural!r}")

		return f"<BaseAccronymEntry{' ' if len(data) > 0 else ''}{' '.join(data)}>"


	def clear(self) -> None:
		self.counter = 0

	def __radd__(self, other):
		if(hasattr(other, '__str__')):
			other = str(other)
		if(isinstance(other, str)):
			return other + self.__str__()
	def __add__(self, other):
		if(hasattr(other, '__str__')):
			other = str(other)
		if(isinstance(other, str)):
			return self.__str__() + other
		
	def __str__(self) -> str:
		self.counter += 1
		if(self.long and self.counter == 1):
			self._registry._used.add(self.short)

			return a(_text(f"{self.long} ({self.short})"), href=self.reference)
		return a(_text(self.short), href=self.reference)
	
	@property
	def short(self) -> str:
		text = self._short
		for fn in self._transformations:
			text = fn(text)

		return text
	@property
	def short_plural(self) -> str:
		text = self._short_plural
		for fn in self._transformations:
			text = fn(text)

		return text
	@property
	def long(self) -> str:
		text = self._long
		for fn in self._transformations:
			text = fn(text)

		return text
	@property
	def long_plural(self) -> str:
		text = self._long_plural
		for fn in self._transformations:
			text = fn(text)

		return text

	@property
	def reference(self):
		return f"#acro.{self.short}"

	@property
	def plural(self):
		return self._plural_cls(self)

	@staticmethod
	def _lower(text: str) -> str:
		return text.lower()
	def lower(self):
		if(BaseAcronymEntry._lower not in self._transformations):
			self._transformations.append(BaseAcronymEntry._lower)

	@staticmethod
	def _upper(text: str) -> str:
		return text.upper()
	def upper(self):
		if(BaseAcronymEntry._upper not in self._transformations):
			self._transformations.append(BaseAcronymEntry._upper)

	@staticmethod
	def _capitalize(text: str) -> str:
		return text.capitalize()
	def capitalize(self):
		if(BaseAcronymEntry._capitalize not in self._transformations):
			self._transformations.append(BaseAcronymEntry._capitalize)


	class _plural_cls:
		_bacr: 'BaseAcronymEntry'=None

		def __init__(self, bacr: 'BaseAcronymEntry') -> None:
			self._bacr = bacr

		def __radd__(self, other):
			if(hasattr(other, '__str__')):
				other = str(other)
			if(isinstance(other, str)):
				return other + self.__str__()
		def __add__(self, other):
			if(hasattr(other, '__str__')):
				other = str(other)
			if(isinstance(other, str)):
				return self.__str__() + other
		
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
