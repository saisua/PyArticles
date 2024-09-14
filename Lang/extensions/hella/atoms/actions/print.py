from typing import *

from ..action import Action

class Print(Action):
	_registered_actions: Dict[str, 'Action']

	_hella: 'Hella'

	_returns: bool=False

	data: Optional['Value']

	def __init__(self, _hella: 'Hella', /, data: Any=None):
		if(data is not None and not isinstance(data, _hella._valueType)):
			data = _hella.new(data)

		super().__init__(_hella)

		self.data = data

	def __init_subclass__(cls) -> None:
		cls._registered_actions[cls.__name__] = cls

	def __repr__(self) -> str:
		if(self.data is not None):
			return f"<Print {self.data}>"
		return "<Print>"

	@property
	def values(self) -> Iterable[Any]:
		if(self.data is not None and hasattr(self.data.data, 'values')):
			return self.data.data.values
		else:
			return []
	
	def render(self) -> Any:
		if(self.data is not None):
			return self.data.render()
		else:
			return True
	
	def render_str(self) -> str:
		if(self.data is not None):
			return f"console.log({self.data.render_str()})"
		return "console.log()"
