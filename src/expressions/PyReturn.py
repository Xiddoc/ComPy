"""
Return statement.
"""
from _ast import Expr

from src.expressions.PyExpression import PyExpression


class PyReturn(PyExpression):
	"""
	Return statement.
	"""

	__value: PyExpression

	def __init__(self, expression: Expr):
		super().__init__(expression)
		# Translate the value
		self.__value = PyExpression.from_ast(expression.value)

	def transpile(self) -> str:
		"""
		Transpiles the constant to a string.
		"""
		return f"return {self.__value.transpile()};"
