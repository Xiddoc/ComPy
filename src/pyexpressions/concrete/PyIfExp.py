"""
Conditional expression.
"""
from _ast import IfExp

from src.pyexpressions.abstract.PyConditional import PyConditional
from src.pyexpressions.abstract.PyExpression import PyExpression
from src.structures.TypeRenames import GENERIC_PYEXPR_TYPE


class PyIfExp(PyConditional):
	"""
	Expression for a Python conditional expression.
	"""

	__else: PyExpression

	def __init__(self, expression: IfExp, parent: GENERIC_PYEXPR_TYPE):
		super().__init__(expression, parent)
		# Send to "else"
		self.__else = expression.orelse

	def _transpile(self) -> str:
		"""
		Transpile the expression to a string.
		"""
		return f"{self.transpile_condition()} ? {self.transpile_body()} : {self.__else.transpile()}"
