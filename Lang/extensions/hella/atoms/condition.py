from typing import *

from abc import abstractmethod
from typing import Any

from .action import Action

registered_conditions: Final[Dict[str, 'Condition']] = []
class Condition:
    _registered_conditions: Dict[str, 'Condition'] = registered_conditions
    _triggered_actions: List[Action]
    _used_values: List['Value']

    name: str
    num_conditions: int=0

    _hella: 'Hella'
    
    def __init__(self, _hella: 'Hella'=None, /, values: Iterable['Value']=[]) -> None:
        if(_hella is not None):
            self._register_hella(_hella)
        self._triggered_actions = list()

        self.name = f'c{Condition.num_conditions}'
        Condition.num_conditions += 1

        self._used_values = list(values)
        for value in values:
            value.register_condition(self)

    def __hash__(self) -> int:
        return hash((self.__class__.__name__, *self._used_values))
    
    def __eq__(self, other) -> bool:
        return self.__hash__() == other.__hash__()
    
    def __bool__(self) -> bool:
        return self.render()
    
    def __contains__(self, value: Union['Value', 'Condition', Action]) -> bool:
        if(isinstance(value, Action)):
            return value in self._triggered_actions

        if(value in self._used_values):
            return True
        
        for used_value in self._used_values:
            if(isinstance(used_value, Condition) and value in used_value):
                return True
        
        return False

    @abstractmethod
    def render(self) -> Any:
        ...
    
    @abstractmethod
    def render_str(self) -> str:
        ...

    def _register_hella(self, _hella: 'Hella') -> None:
        self._hella = _hella
        self._hella._conditions.append(self)

    def trigger(self, actions: Action | Iterable[Action]) -> Any:
        if(isinstance(actions, Action)):
            self._triggered_actions.append(actions)
        elif(isinstance(actions, Iterable)):
            self._triggered_actions.extend(actions)
        
    @classmethod
    def get_condition(cls, name: str) -> 'Condition':
        return cls._registered_conditions[name]
    
    # class Add:
    # class Sub:
    # class Mul:
    # class Div:
    # class Pow:
    # class Lt:
    # class Gt:
    # class Le:
    # class Ge:
    # class Eq:
    # class Ne:
    # class And:
    # class Or:
    # class Xor:
    # class Not:
    # class Is:
    # class IsNot:
    # class In:
    # class NotIn:
    # class IsNone:
    # class IsNotNone:
    # class IsEmpty:
    # class IsNotEmpty:
    # class IsTrue:
    # class IsFalse:
    # class IsNone:
    # class IsNotNone:
    # class IsEmpty:
    # class IsNotEmpty:
    # class IsTrue:
    # class IsFalse: