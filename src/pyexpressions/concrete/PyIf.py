"""
Class for a conditional statement.
"""
from _ast import IfExp

from src.pyexpressions.abstract.PyConditional import PyConditional
from src.structures.TypeRenames import GENERIC_PYEXPR_TYPE


class PyIf(PyConditional):
	"""
	Class for a Python conditional statement.
	"""

	def __init__(self, expression: IfExp, parent: GENERIC_PYEXPR_TYPE):
		super().__init__(expression, "if", parent)
