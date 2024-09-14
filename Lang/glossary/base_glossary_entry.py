from Lang.text.text import _text

from Lang.compatibility import *

class BaseGlossaryEntry(_text):
	_name: str
	description: Optional[str]

	_transformations: List[Callable]

	def __init__(self, name: str, description: Optional[str]=None) -> None:
		self._name = name
		self.description = description

		self._transformations = list()

		super().__init__(self.name)


	def __repr__(self) -> str:
		if(self.description is not None):
			short_desc: str
			if len(self.description) > 15:
				short_desc = self.description[:15] + '...'
			else:
				short_desc = self.description
			return f"<BaseGlossaryEntry name={self._name} description={short_desc}>"
		return f"<BaseGlossaryEntry name={self._name}>"
	
	@property
	def name(self) -> str:
		text = self._name
		for fn in self._transformations:
			text = fn(text)

		return text

	def __call__(self, doc: 'Document', mode: str | int=None) -> str:
		return self.name

	def __str__(self) -> str:
		return self.name
	
	def render(self) -> str:
		return f"{self.name}: {self.description or ''}"


	@staticmethod
	def _lower(text: str) -> str:
		return text.lower()
	def lower(self):
		if(BaseGlossaryEntry._lower not in self._transformations):
			self._transformations.append(BaseGlossaryEntry._lower)

	@staticmethod
	def _upper(text: str) -> str:
		return text.upper()
	def upper(self):
		if(BaseGlossaryEntry._upper not in self._transformations):
			self._transformations.append(BaseGlossaryEntry._upper)

	@staticmethod
	def _capitalize(text: str) -> str:
		return text.capitalize()
	def capitalize(self):
		if(BaseGlossaryEntry._capitalize not in self._transformations):
			self._transformations.append(BaseGlossaryEntry._capitalize)
