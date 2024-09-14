from Lang.html.base_tag import BaseTag, Block

from Lang.extensions.hella.atoms.actions import TestConditions, Action
from Lang.extensions.hella.atoms.condition import Condition

from Lang.compatibility import *

class checkbox(Condition, BaseTag):
	def __init__(self, next_blocks: List[Block] | None = None, *args, **kwargs) -> None:
		if('type' not in kwargs):
			kwargs['type'] = 'checkbox'
		BaseTag.__init__(self, 'input', *args, next_blocks=next_blocks, **kwargs)
		Condition.__init__(self)
		

	def trigger(self, action: Action) -> Any:
		self._register_hella(action._hella)

		if(not any((True for after in action._run_after if isinstance(after, TestConditions)))):
			action._run_after.append(TestConditions(action._hella))
		if('event' not in action._hella_args):
			action._hella_args.append('event')

		self._kwargs['py-click'] = f"{action.name}"
		Condition.trigger(self, action)

	def on_click(self, action: Action):
		self.trigger(action)