from typing import *
from abc import abstractmethod

registered_actions: Dict[str, 'Action'] = dict()
class Action:
	_registered_actions: Dict[str, 'Action'] = dict()

	num_actions: int = 0
	name: str

	_returns: bool=True
	
	_run_after: List[Any]

	_hella: 'Hella'

	_hella_args: List[str]
	_hella_kwargs: List[str]

	def __init__(self, _hella: 'Hella', /, updated_values: Iterable['Value']=[]) -> None:
		self._hella = _hella

		self.name = f'a{Action.num_actions}'
		Action.num_actions += 1

		for value in updated_values:
			value._acted_upon = True

		self._hella._actions.append(self)
		self._run_after = list()

		self._hella_args = list()
		self._hella_kwargs = list()

	def __hash__(self) -> int:
		return hash((self.__class__.__name__, *self.values))

	@abstractmethod
	def __repr__(self) -> str:
		...

	@abstractmethod
	def render(self) -> Any:
		...
	
	@abstractmethod
	def render_str(self) -> str:
		...

	@abstractmethod
	def values(self) -> Iterable[Any]:
		...

	@classmethod
	def get_action(cls, name: str) -> 'Action':
		return cls._registered_actions[name]