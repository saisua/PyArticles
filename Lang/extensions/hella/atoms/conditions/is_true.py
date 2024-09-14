from typing import *
from ..condition import Condition
from ..action import Action

class isTrue(Condition):
    _registered_conditions: Dict[str, 'Condition']
    _triggered_actions: List[Action]
    _used_values: List['Value']

    _hella: 'Hella'
    data: Any
    def __init__(self, _hella: 'Hella', /, data: Any) -> None:
        if(not isinstance(data, _hella._valueType)):
            data = _hella.new(data)
        self.data = data

        super().__init__(_hella, values=[data])

    def __init_subclass__(cls) -> None:
        cls._registered_conditions[cls.__name__] = cls
    
    def __repr__(self) -> str:
        return f"<isTrue {self.data!r}>"

    def render(self) -> Any:
        return bool(self.data.render())
    
    def render_str(self) -> str:
        return f"bool({self.data.render_str()})"
