try:
	from enum import StrEnum
except ImportError:
	...

from Lang.compatibility import *

class Symbols(StrEnum):
	ABSOLUTE_SYMBOL = '|'
	ADDITION_SYMBOL = '+'
	SUBTRACTION_SYMBOL = '-'
	MULIPLICATION_SYMBOL = 'x'
	DIVISION_SYMBOL = '/'
	CIRCLE_ADD_SYMBOL = '⊕'
	CIRCLE_SUBTRACT_SYMBOL = '⊖'
	CICRLE_PRODUCT_SYMBOL = '⊗'
	CICRLE_SLASH_SYMBOL = '⊘'
	CICRLE_EQUALS_SYMBOL = '⊜'

	ALL_SYMBOL = '∀'
	PARTIAL_DERIVATIVE_SYMBOL = '∂'
	EXISTS_SYMBOL = '∃'
	NOT_EXISTS_SYMBOL = '∄'
	EMPTY_SET_SYMBOL = '∅'
	NABLA_SYMBOL = '∇'
	IN_SYMBOL = '∈'
	NOT_IN_SYMBOL = '∉'
	ELEMENT_SYMBOL = '∋'
	NOT_ELEMENT_SYMBOL = '∌'

	PRODUCT_SYMBOL = '∏'
	COPRODUCT_SYMBOL = '∐'

	MINUS_SYMBOL = '−'
	PLUS_MINUS_SYMBOL = '∓'
	ROOT_SYMBOL = '√'
	PROPORTIONAL_SYMBOL = '∝'
	INFINITE_SYMBOL = '∞'

	AND_SET_SYMBOL = '∧'
	OR_SET_SYMBOL = '∨'
	UNION_SET_SYMBOL = '∪'
	INTERSECTION_SET_SYMBOL = '∩'
	SUBSET_SYMBOL = '⊂'
	SUPERSET_SYMBOL = '⊃'
	NOT_SUBSET_SYMBOL = '⊄'
	NUT_SUPERSET_SYMBOL = '⊅'

	INTEGRAL_SYMBOL = '∫'

	THEREFORE_SYMBOL = '∴'
	BECAUSE_SYMBOL = '∵'
	RATIO_SYMBOL = '∶'
	APPROXIMATION_SYMBOL = '∽'

	WALRUS_SYMBOL = '≔'
	EQUALS_SYMBOL = '='
	NOT_EQUALS_SYMBOL = '≠'
	GREATER_THAN_SYMBOL = '>'
	LESS_THAN_SYMBOL = '<'
	GREATER_OR_EQUAL_TO = '≥'
	LESS_OR_EQUAL_TO = '≤'
	MUCH_LESS_THAN = '≪'
	MUCH_GREATER_THAN = '≫'

	CAPITAL_ALPHA_SYMBOL = 'Α'
	CAPITAL_BETA_SYMBOL = 'Β'
	CAPITAL_GAMMA_SYMBOL = 'Γ'
	CAPITAL_DELTA_SYMBOL = 'Δ'
	CAPITAL_EPSILON_SYMBOL = 'Ε'
	CAPITAL_ZETA_SYMBOL = 'Ζ'
	CAPITAL_ETA_SYMBOL = 'Η'
	CAPITAL_THETA_SYMBOL = 'Θ'
	CAPITAL_IOTA_SYMBOL = 'Ι'
	CAPITAL_KAPPA_SYMBOL = 'Κ'
	CAPITAL_LAMBDA_SYMBOL = 'Λ'
	CAPITAL_MU_SYMBOL = 'Μ'
	CAPITAL_NU_SYMBOL = 'Ν'
	CAPITAL_XI_SYMBOL = 'Ξ'
	CAPITAL_OMICRON_SYMBOL = 'Ο'
	CAPITAL_PI_SYMBOL = 'Π'
	CAPITAL_RHO_SYMBOL = 'Ρ'
	CAPITAL_SIGMA_SYMBOL = 'Σ'
	CAPITAL_TAU_SYMBOL = 'Τ'
	CAPITAL_UPSILON_SYMBOL = 'Υ'
	CAPITAL_PHI_SYMBOL = 'Φ'
	CAPITAL_CHI_SYMBOL = 'Χ'
	CAPITAL_PSY_SYMBOL = 'Ψ'
	CAPITAL_OMEGA_SYMBOL = 'Ω'

	ALPHA_SYMBOL = 'α'
	BETA_SYMBOL = 'β'
	GAMMA_SYMBOL = 'γ'
	DELTA_SYMBOL = 'δ'
	EPSILON_SYMBOL = 'ε'
	ZETA_SYMBOL = 'ζ'
	ETA_SYMBOL = 'η'
	THETA_SYMBOL = 'θ'
	IOTA_SYMBOL = 'ι'
	KAPPA_SYMBOL = 'κ'
	LAMBDA_SYMBOL = 'λ'
	MU_SYMBOL = 'μ'
	NU_SYMBOL = 'ν'
	XI_SYMBOL = 'ξ'
	OMICRON_SYMBOL = 'ο'
	PI_SYMBOL = 'π'
	RHO_SYMBOL = 'ρ'
	SIGMA_SYMBOL = 'σ'
	TAU_SYMBOL = 'τ'
	UPSILON_SYMBOL = 'υ'
	PHI_SYMBOL = 'φ'
	CHI_SYMBOL = 'χ'
	PSY_SYMBOL = 'ψ'
	OMEGA_SYMBOL = 'ω'

	KILO_SYMBOL = 'k'
	MILI_SYMBOL = 'm'
	NANO_SYMBOL = 'n'
	FEMTO_SYMBOL = 'f'
	ATTO_SYMBOL = 'a'

	NATURAL_NUMBERS_SYMBOL = 'ℕ'
	INTEGER_NUMBERS_SYMBOL = 'ℤ'
	RATIONAL_NUMBERS_SYMBOL = 'ℚ'
	REAL_NUMBERS_SYMBOL = 'ℝ'
	COMPLEX_NUMBERS_SYMBOL = 'ℂ'
	QUATERNIONS_SYMBOL = 'ℍ'
	FINITE_FIELDS_SYMBOL = '𝔽'
	OCTONIONS_SYMBOL = '𝕆'

	ARROW_RIGHT_SYMBOL = '→'
	ARROW_LEFT_SYMBOL = '←'
	ARROW_UP_SYMBOL = '↑'
	ARROW_DOWN_SYMBOL = '↓'
	ARROW_UP_RIGHT_SYMBOL = '↗'
	ARROW_UP_LEFT_SYMBOL = '↖'
	ARROW_DOWN_RIGHT_SYMBOL = '↘'
	ARROW_DOWN_LEFT_SYMBOL = '↙'
	ARROW_RIGHT_LEFT_SYMBOL = '↔'
	ARROW_UP_DOWN_SYMBOL = '↕'
	ARROW_RIGHTWARDS_ARROW_WITH_HOOK = '↪'
	ARROW_LEFTWARDS_ARROW_WITH_HOOK = '↩'
	ARROW_RIGHTWARDS_BROKEN_ARROW = '↷'
	ARROW_LEFTWARDS_BROKEN_ARROW = '↶'
	ARROW_CLOCKWISE = '↻'
	ARROW_COUNTERCLOCKWISE = '↺'
	ARROW_RIGHTWARDS_DOUBLE_ARROW = '⇒'
	ARROW_LEFTWARDS_DOUBLE_ARROW = '⇐'
	ARROW_UPWARDS_DOUBLE_ARROW = '⇑'
	ARROW_DOWNWARDS_DOUBLE_ARROW = '⇓'
	ARROW_RIGHTWARDS_TRIPLE_ARROW = '⇛'
	ARROW_LEFTWARDS_TRIPLE_ARROW = '⇚'
	ARROW_RIGHTWARDS_DOTTED_ARROW = '⇢'
	ARROW_LEFTWARDS_DOTTED_ARROW = '⇠'
	ARROW_UP_DOTTED_ARROW = '⇡'
	ARROW_DOWN_DOTTED_ARROW = '⇣'
	ARROW_ZIGZAG_RIGHT = '↝'
	ARROW_ZIGZAG_LEFT = '↜'
	ARROW_RIGHTWARDS_SWEEP_ARROW = '⇉'
	ARROW_LEFTWARDS_SWEEP_ARROW = '⇇'
	ARROW_UP_RIGHT_QUADRUPLE_ARROW = '⇗'
	ARROW_UP_LEFT_QUADRUPLE_ARROW = '⇖'
	ARROW_DOWN_RIGHT_QUADRUPLE_ARROW = '⇘'
	ARROW_DOWN_LEFT_QUADRUPLE_ARROW = '⇙'
	ARROW_LONG_RIGHTWARDS = '⟶'
	ARROW_LONG_LEFTWARDS = '⟵'
	ARROW_LONG_UPWARDS = '⟰'
	ARROW_LONG_DOWNWARDS = '⟱'
	ARROW_HEAVY_RIGHTWARDS = '➡'
	ARROW_HEAVY_LEFTWARDS = '⬅'
	ARROW_HEAVY_UPWARDS = '⬆'
	ARROW_HEAVY_DOWNWARDS = '⬇'
	ARROW_RIGHTWARDS_SQUIGGLE = '➝'
	ARROW_LEFTWARDS_SQUIGGLE = '➜'
	ARROW_RIGHT_TILDE_ARROW = '⇛'
	ARROW_LEFT_TILDE_ARROW = '⇚'
	ARROW_UP_HEAVY_LINE_ARROW = '⇧'
	ARROW_DOWN_HEAVY_LINE_ARROW = '⇩'
	ARROW_CLOCKWISE_OPEN_CIRCLE = '↻'
	ARROW_COUNTERCLOCKWISE_OPEN_CIRCLE = '↺'
	ARROW_RIGHTWARDS_CURVED_ARROW = '↬'
	ARROW_LEFTWARDS_CURVED_ARROW = '↫'
	ARROW_UP_HEAVY_ARROW = '⇑'
	ARROW_DOWN_HEAVY_ARROW = '⇓'
	ARROW_RIGHTWARDS_TRIANGLE_ARROW = '⊳'
	ARROW_LEFTWARDS_TRIANGLE_ARROW = '⊲'
	ARROW_RIGHTWARDS_OPEN_ARROW = '⇥'
	ARROW_LEFTWARDS_OPEN_ARROW = '⇤'
	ARROW_RIGHTWARDS_WHITE_ARROW = '⇨'
	ARROW_LEFTWARDS_WHITE_ARROW = '⇦'
	ARROW_HALF_TOP_RIGHT_ARROW = '⇀'
	ARROW_HALF_BOTTOM_RIGHT_ARROW = '⇁'
	ARROW_HALF_TOP_LEFT_ARROW = '↼'
	ARROW_HALF_BOTTOM_LEFT_ARROW = '↽'
	ARROW_HALF_LEFT_UP_ARROW = '↿'
	ARROW_HALF_RIGHT_UP_ARROW = '↾'
	ARROW_HALF_LEFT_DOWN_ARROW = '⇃'
	ARROW_HALF_RIGHT_DOWN_ARROW = '⇂'
	ARROW_HALF_RIGHT_DOWN_ARROW = '⇂'
	ARROW_HALF_RIGHT_DOWN_ARROW = '⇂'


class SymbolAliases:
	SUM_SYMBOL = Symbols.CAPITAL_SIGMA_SYMBOL

	MICRO_SYMBOL = Symbols.MU_SYMBOL
	PICO_SYMBOL = Symbols.RHO_SYMBOL

	BOOL_SYMBOL = f"{Symbols.INTEGER_NUMBERS_SYMBOL}{Symbols.IN_SYMBOL}{{0,1}}"
	INT_SYMBOL = Symbols.INTEGER_NUMBERS_SYMBOL
	FLOAT_SYMBOL = Symbols.REAL_NUMBERS_SYMBOL
	DOUBLE_SYMBOL = Symbols.REAL_NUMBERS_SYMBOL

	CONCATENATION_SYMBOL = Symbols.CIRCLE_ADD_SYMBOL

	FUNCTIONAL_DERIVATIVE_SYMBOL = Symbols.DELTA_SYMBOL
	DERIVATIVE_SYMBOL = Symbols.PARTIAL_DERIVATIVE_SYMBOL

	GRADIENT_SYMBOL = Symbols.NABLA_SYMBOL

	ASSIGNMENT_SYMBOL = Symbols.ARROW_LEFT_SYMBOL


class SpecialSymbols:
	...

globals().update(dict(filter(lambda x: not x[0].startswith('_'), Symbols.__dict__.items())))
globals().update(dict(filter(lambda x: not x[0].startswith('_'), SymbolAliases.__dict__.items())))
globals().update(dict(filter(lambda x: not x[0].startswith('_'), SpecialSymbols.__dict__.items())))
