"""
Expression statement.
"""
from _ast import Expr, Constant
from typing import Union, Type, Optional

from src.Constants import GENERIC_PYEXPR_TYPE
from src.pyexpressions.PyExpression import PyExpression


class PyExpr(PyExpression):
	"""
	Expression statement.
	"""

	__value: Optional[PyExpression]

	def __init__(self, expression: Expr, parent: GENERIC_PYEXPR_TYPE):
		super().__init__(expression, parent)
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
