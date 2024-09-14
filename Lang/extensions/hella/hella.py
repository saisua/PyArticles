from typing import *
import os

from Lang.document import Document
from Lang.html.script import script

import numpy as np
import aiofiles

from .atoms.actions import *
from .atoms.conditions import *

from .atoms.value import Value

class Hella:
	_actions: List[Action]
	_conditions: List[Condition]

	_call_masks: np.ndarray

	_valueType: Final[TypeVar] = Value

	def __init__(self) -> None:
		self._conditions = list()
		self._actions = list()

	async def __call__(self, document: Document, *args: Any, mode: str | int=None, **kwds: Any) -> Any:
		document.add_script(filename="https://pyscript.net/releases/2024.6.1/core.js", type="module")

		script_path = f'{document.path}/static/hella.py'

		rendered_data: str = self.render()
		if(os.path.exists(script_path)):
			existing_data: str
			async with aiofiles.open(script_path, 'r') as f:
				existing_data = await f.read()

			if(existing_data == rendered_data):
				rendered_data = None

		if(rendered_data):
			async with aiofiles.open(script_path, 'w+') as f:
				await f.write(rendered_data)

		document._next.append(script(filename='hella.py', type='py'))

	def render(self) -> str:
		import_lines: List[str] = [
			"from js import console",
			"from pyscript import document"
		]
		code_lines: List[str] = ["def test_conditions():"]

		created_modified_values: Set[Value] = set()
		created_actions: Dict[Action, Set[Value]] = dict()
		condition_lines_buffer: Dict[Condition, List[str]] = {}
		for condition in self._conditions:
			if(not hasattr(condition, 'render_str')):
				continue

			cond_lines: List[str] = condition_lines_buffer.get(condition)
			if(cond_lines is None):
				# print(f"Got new condition {condition!r}")
				cond_lines = []
				condition_lines_buffer[condition] = cond_lines
			# else:
			# 	print(f"Got already existing condition {condition!r}")

			for triggered_action in condition._triggered_actions:
				cond_lines.append(f"\t\t{triggered_action.name}()")

				action_conditions: Set[Action] = set()
				action_values: Set[Value] = set()
				for value in triggered_action.values:
					if(value._acted_upon or value._force_var):
						created_modified_values.add(value)
						action_values.add(value)

					for condition in value._condition_refs:
						action_conditions.add(condition)


				if(triggered_action in created_actions):
					created_actions[triggered_action].update(action_values)
				else:
					created_actions[triggered_action] = action_values

				# for action_condition in action_conditions:
				#     code_lines.append(f"---> {action_condition.render_str()}")

		first_condition: bool = True
		for condition, condition_lines in condition_lines_buffer.items():
			if(not condition_lines):
				continue

			str_cond = condition.render_str()
			
			if(not str_cond):
				continue
			
			if(first_condition):
				code_lines.append(f"\tif {str_cond}:")

				first_condition = False
			else:
				code_lines.append(f"\telif {str_cond}:")
			
			code_lines.extend(condition_lines)
			code_lines.append(f"\t\tconsole.log({','.join((v.name for v in created_modified_values))})")
			code_lines.append(f"\t\ttest_conditions()")

		define_action_lines = []
		for action, updated_values in created_actions.items():
			action_params = [*action._hella_args, '*args', *action._hella_kwargs, '**kwargs']
			
			define_action_lines.append(f"def {action.name}({','.join(action_params)}):")
			if(updated_values):
				define_action_lines.append(f"\tglobal {','.join((v.name for v in updated_values))}")

			if(action._returns):
				if(not action._run_after):
					define_action_lines.append(f"\treturn {action.render_str()}")
				else:
					define_action_lines.extend((
						f"\tresult = {action.render_str()}",
						*(f"\t{after.render_str()}" for after in action._run_after),
						"\treturn result",
					))
			else:
				define_action_lines.append(f"\t{action.render_str()}")
				define_action_lines.extend([f"\t{after.render_str()}" for after in action._run_after])

		define_var_lines = []
		for value in created_modified_values:
			define_var_lines.append(f"{value.name} = {value.render_str(force_render_str=True)}")

		code_lines.insert(1, f"\tglobal {','.join((v.name for v in created_modified_values))}")
		
		return '\n'.join(import_lines) + "\n" +\
			"\n".join(define_var_lines) + "\n" +\
			"\n".join(define_action_lines) + "\n" +\
			"\n".join(code_lines) + "\n" +\
			"test_conditions()"
	
	def new(self, data: Any) -> Value:
		return Value(self, data)
	
	def new_code(self, data: Any) -> Value:
		code = self.new(data)
		code._repr_data = False

		return code