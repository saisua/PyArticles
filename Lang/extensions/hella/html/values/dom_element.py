from Lang.html.base_tag import BaseTag, Block

from Lang.extensions.hella.atoms.value import Value
from Lang.extensions.hella.html.actions.set_style import SetStyle
from Lang.extensions.hella.html.actions.remove_style import RemoveStyle


from Lang.compatibility import *

class dom_element(Value):
	_dom_id: int | str
	
	data: BaseTag | str

	_repr_data: bool=False
	_force_var: bool=True

	def __init__(self, _hella, data: BaseTag | str, *args, id: int | str=None, **kwargs) -> None:
		if(id is None):
			if(isinstance(data, BaseTag)):
				id = data.id
			else:
				id = data

		self._dom_id = id

		Value.__init__(self, _hella, data)

	
	def render_str(self, force_render_str: bool = False) -> Any:
		if((self._acted_upon or self._force_var) and not self._return_render_str and not force_render_str):
			return self.name
		
		data_value = f"document.getElementById(\"{self._dom_id}\")"

		if(self._repr_data):
			return repr(data_value)
		else:
			return str(data_value)
		
	def set_style(self, style_key: str, style_value: str) -> SetStyle:
		return SetStyle(self._hella, self, style_key, style_value)

	def remove_style(self, style_key: str) -> RemoveStyle:
		return RemoveStyle(self._hella, self, style_key)