from typing import *

from Lang.formulas.base_var import BaseVar
from Lang.formulas.mathml.html.math import math

def formula(var: BaseVar):
	return math(var.render())