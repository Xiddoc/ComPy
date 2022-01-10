"""
Expression statement.
"""
from _ast import Expr, Constant
from typing import Union

from src.pyexpressions.PyExpression import PyExpression


class PyExpr(PyExpression):
	"""
	Expression statement.
	"""

	__value: Union[PyExpression, None]

	def __init__(self, expression: Expr):
		super().__init__(expression)
		# Make sure it is not a multiline Python string
		# If the node itself is an expression
		if type(expression.value) == Constant:
			# Then skip this node
			self.__value = None
		else:
			# Otherwise, translate the value
			self.__value = self.from_ast(expression.value)

	def transpile(self) -> str:
		"""
		Transpiles the constant to a string.
		"""
		return self.__value.transpile() if self.__value else ""
