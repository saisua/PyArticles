from typing import *

from ..action import Action

class TestConditions(Action):
	_registered_actions: Dict[str, 'Action']

	_hella: 'Hella'

	_returns: bool=False

	data: Optional['Value']

	def __init__(self, _hella: 'Hella', /, data: Any=None):
		if(data is not None):
			if(not isinstance(data, _hella._valueType)):
				data = _hella.new(data)

			super().__init__(_hella, updated_values=[data])
		else:
			super().__init__(_hella)

		self.data = data

	def __init_subclass__(cls) -> None:
		cls._registered_actions[cls.__name__] = cls

	def __repr__(self) -> str:
		if(self.data is not None):
			return f"<TestConditions after {self.data}>"
		return "<TestConditions>"

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
		return "test_conditions()"
