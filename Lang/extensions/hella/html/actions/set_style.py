from typing import *

from Lang.extensions.hella.atoms.action import Action

class SetStyle(Action):
	_registered_actions: Dict[str, 'Action']

	_hella: 'Hella'

	_returns: bool=False

	target: Any
	key: Any
	value: Any

	def __init__(self, _hella: 'Hella', /, target: Any, key: Any, value: Any):
		if(not isinstance(target, _hella._valueType)):
			target = _hella.new(target)
		if(not isinstance(key, _hella._valueType)):
			key = _hella.new(key)
		if(not isinstance(value, _hella._valueType)):
			value = _hella.new(value)

		self.target = target
		self.key = key
		self.value = value

		super().__init__(_hella)

	def __init_subclass__(cls) -> None:
		cls._registered_actions[cls.__name__] = cls

	def __repr__(self) -> str:
		return f"<SetStyle {self.target!r}[{self.key!r}] = {self.value!r}>"

	@property
	def values(self) -> Iterable[Any]:
		yield from (self.target, self.key, self.value)

	def render(self) -> Any:
		style_value = self.value.render()
		self.target.render().style[self.key.render()] = style_value

		return style_value
	
	def render_str(self) -> str:
		return f"{self.target.render_str()}.style.visible = {self.value.render_str()}"
