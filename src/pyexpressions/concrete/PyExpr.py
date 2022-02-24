"""
Expression statement.
"""
from _ast import Expr, Constant

from src.pyexpressions.abstract.PyExpression import PyExpression
from src.structures.TypeRenames import GENERIC_PYEXPR_TYPE


class PyExpr(PyExpression):
	"""
	Expression statement.
	"""

	__value: PyExpression
	__is_empty_expr: bool

	def __init__(self, expression: Expr, parent: GENERIC_PYEXPR_TYPE):
		super().__init__(expression, parent)
		# Convert value and assign to field
		self.__value = self.from_ast(expression.value)
		# If the entire expression is just a constant literal,
		# then mark this expression as empty (no code runs here)
		self.__is_empty_expr = isinstance(expression.value, Constant)

	def is_empty_expression(self) -> bool:
		"""
		:return: True if this expression does not execute code, False if it does execute code.
		"""
		return self.__is_empty_expr

	def _transpile(self) -> str:
		"""
		Transpile the operation to a string.
		"""
		return self.__value.transpile()
