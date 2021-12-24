"""
Expression statement.
"""
from _ast import Expr
from typing import List

from src.expressions.PyExpression import PyExpression
from src.expressions.PyName import PyName


class PyCall(PyExpression):
	"""
	Expression statement.
	"""

	__args: List[PyExpression]
	__func: PyName

	def __init__(self, expression: Expr):
		super().__init__(expression)
		# Convert and store
		self.__func = PyName(expression.func)
		self.__args = [PyExpression.from_ast(arg) for arg in expression.args]

	def transpile(self) -> str:
		"""
		Transpiles the constant to a string.
		"""
		# Take function name
		# Add parenthesis
		# For each argument, transpile
		# Join the arguments together with commas
		# FUNC_NAME ( ARG1 , ARG2 , ... )
		return f"{self.__func.transpile()}({','.join([arg.transpile() for arg in self.__args])})"
