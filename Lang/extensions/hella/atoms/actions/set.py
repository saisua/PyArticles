from typing import *

from ..action import Action

class Set(Action):
    _registered_actions: Dict[str, 'Action']

    _hella: 'Hella'

    d1: Any
    d2: Any

    def __init__(self, _hella: 'Hella', /, d1: Any, d2: Any):
        if(not isinstance(d1, _hella._valueType)):
            d1 = _hella.new(d1)
        if(not isinstance(d2, _hella._valueType)):
            d2 = _hella.new(d2)

        self.d1 = d1
        self.d2 = d2

        super().__init__(_hella, updated_values=[d1])

    def __init_subclass__(cls) -> None:
        cls._registered_actions[cls.__name__] = cls

    def __repr__(self) -> str:
        return f"<Set {self.d1!r} = {self.d2!r}>"

    @property
    def values(self) -> Iterable[Any]:
        yield from (self.d1, self.d2)

    def render(self) -> Any:
        return self.d2
    
    def render_str(self) -> str:
        return f"({self.d1.render_str()} := {self.d2.render_str()})"
