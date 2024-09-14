from typing import *

from .actions import Add, Set as SetValue, Action
from .conditions import isTrue, lessThan, And, Eq, Condition

class Value:
	_hella: 'Hella'
	name: str
	data: Any

	num_values: int = 0

	# TODO: change to set, to keep unique
	_condition_refs: List[Condition]
	_acted_upon: bool=False
	_return_render_str: bool=False
	_repr_data: bool=True
	_force_var: bool=False

	__var_hash: int
	__data_hash: int

	def __init__(self, _hella: 'Hella', /, data: Any) -> None:
		self._hella = _hella
		self.data = data

		self.name = f'v{Value.num_values}'
		Value.num_values += 1

		self.__var_hash = hash(self.name)
		self.__data_hash = hash(self.data)

		self._condition_refs = list()

	def __hash__(self) -> int:
		if self._acted_upon:
			return self.__var_hash
		return self.__data_hash

	def __repr__(self) -> str:
		if(self._acted_upon):
			return f"<Value {self.name} = {self.data!r}>"
		return f"<Value [const] {self.name} = {self.data!r}>"
	
	def __bool__(self) -> isTrue:
		return isTrue(self._hella, self)

	def __add__(self, data: Any) -> Add:
		return Add(self._hella, self, data)
		
	def __radd__(self, data: Any) -> Add:
		return Add(self._hella, data, self)
	
	def __sub__(self, data: Any) -> Action:
		...

	def __rsub__(self, data: Any) -> Action:
		...

	def __mul__(self, data: Any) -> Action:
		...

	def __rmul__(self, data: Any) -> Action:
		...

	def __truediv__(self, data: Any) -> Action:
		...
		
	def __rtruediv__(self, data: Any) -> Action:
		...
	
	def __div__(self, data: Any) -> Action:
		...
	
	def __rdiv__(self, data: Any) -> Action:
		...

	def __pow__(self, data: Any) -> Action:
		...
	
	def __lt__(self, data: Any) -> lessThan:
		return lessThan(self._hella, self, data)
	
	def __gt__(self, data: Any) -> Condition:
		...
	
	def __le__(self, data: Any) -> Condition:
		...
	
	def __ge__(self, data: Any) -> Condition:
		...
	
	def __eq__(self, data: Any) -> Condition:
		return Eq(self._hella, self, data)
	
	def __ne__(self, data: Any) -> Condition:
		...
	
	def __and__(self, data: Any) -> Condition:
		return And(self._hella, self, data)
	
	def __rand__(self, data: Any) -> Condition:
		return And(self._hella, data, self)

	def __or__(self, value: Any) -> Condition:
		pass

	def __xor__(self, value: Any) -> Condition:
		pass

	def __invert__(self, value: Any) -> Action:
		pass

	def __lshift__(self, value: Any) -> Action:
		pass

	def __rshift__(self, value: Any) -> Action:
		pass

	def __mod__(self, value: Any) -> Action:
		pass

	def __invert__(self, value: Any) -> Action:
		pass

	def set(self, value: Any) -> SetValue:
		return SetValue(self._hella, self, value)

	def register_condition(self, condition: Condition) -> None:
		self._condition_refs.append(condition)

	def register_conditions(self, conditions: Iterable[Condition]) -> None:
		self._condition_refs.extend(conditions)

	def render(self) -> Any:
		if(hasattr(self.data, 'render')):
			return self.data.render()
		else:
			return self.data
		
	def render_str(self, force_render_str: bool = False) -> Any:
		if((self._acted_upon or self._force_var) and not self._return_render_str and not force_render_str):
			return self.name
		elif(hasattr(self.data, 'render_str')):
			return self.data.render_str()
		elif(self._repr_data):
			return repr(self.data)
		else:
			return str(self.data)