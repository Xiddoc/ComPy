"""
Expression statement.
"""
from _ast import Expr

from expressions.PyExpression import PyExpression


class PyExpr(PyExpression):
	"""
	Expression statement.
	"""

	def __init__(self, expression: Expr):
		super().__init__(expression)
		# Translate the value
		self.__value = PyExpression.from_ast(expression.value)

	def transpile(self) -> str:
		"""
		Transpiles the constant to a string.
		"""
		return self.__value.transpile()
