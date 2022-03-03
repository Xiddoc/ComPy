"""
Class for a conditional looped statement.
"""
from _ast import While

from src.pyexpressions.abstract.PyConditional import PyConditional
from src.structures.TypeRenames import GENERIC_PYEXPR_TYPE


class PyWhile(PyConditional):
	"""
	Class for a Python conditional looped statement (while statement).
	"""

	def __init__(self, expression: While, parent: GENERIC_PYEXPR_TYPE):
		super().__init__(expression, parent)

	def _transpile(self) -> str:
		"""
		Transpile the conditional statement to a string.
		"""
		return "while " + super()._transpile()
