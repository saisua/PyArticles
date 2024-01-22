from typing import *

class BaseGlossaryEntry:
	name: str
	description: Optional[str]

	def __init__(self, name: str, description: Optional[str]=None) -> None:
		self.name = name
		self.description = description

	def __str__(self) -> str:
		return self.name
	
	def render(self) -> str:
		return f"{self.name}: {self.description or ''}"