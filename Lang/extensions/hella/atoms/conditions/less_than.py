from typing import *
from ..condition import Condition
from ..action import Action

class lessThan(Condition):
    _registered_conditions: Dict[str, 'Condition']
    _triggered_actions: List[Action]
    _used_values: List['Value']

    _hella: 'Hella'
    d1: Any
    def __init__(self, _hella: 'Hella', /, d1: Any, d2: Any) -> None:
        if(not isinstance(d1, _hella._valueType)):
            d1 = _hella.new(d1)
        if(not isinstance(d2, _hella._valueType)):
            d2 = _hella.new(d2)
        
        self.d1 = d1
        self.d2 = d2

        super().__init__(_hella, values=[d1,d2])

    def __init_subclass__(cls) -> None:
        cls._registered_conditions[cls.__name__] = cls

    def __repr__(self) -> str:
        return f"<lessThan d1={self.d1!r} d2={self.d2!r}>"

    def render(self) -> Any:
        return self.d1.render() < self.d2.render()
    
    def render_str(self) -> str:
        return f"({self.d1.render_str()} < {self.d2.render_str()})"
