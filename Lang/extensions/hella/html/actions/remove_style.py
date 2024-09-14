from typing import *

from Lang.extensions.hella.atoms.action import Action

class RemoveStyle(Action):
	_registered_actions: Dict[str, 'Action']

	_hella: 'Hella'
	
	target: Any
	key: Any

	def __init__(self, _hella: 'Hella', /, target: Any, key: Any):
		if(not isinstance(target, _hella._valueType)):
			target = _hella.new(target)
		if(not isinstance(key, _hella._valueType)):
			key = _hella.new(key)

		self.target = target
		self.key = key

		super().__init__(_hella)

	def __init_subclass__(cls) -> None:
		cls._registered_actions[cls.__name__] = cls

	def __repr__(self) -> str:
		return f"<RemoveStyle {self.target!r}[{self.key!r}]>"

	@property
	def values(self) -> Iterable[Any]:
		yield from (self.target, self.key)

	def render(self) -> Any:
		style_value = self.value.render()
		self.target.render().style[self.key.render()] = style_value

		return style_value
	
	def render_str(self) -> str:
		return f"{self.target.render_str()}.style.pop({self.key.render_str()})"
