"""
Return statement.
"""
from _ast import Return

from src.Compiler import Compiler
from src.pyexpressions.PyExpression import PyExpression


class PyReturn(PyExpression):
	"""
	Return statement.
	"""

	__value: PyExpression

	def __init__(self, expression: Return):
		super().__init__(expression)
		# Translate the value
		self.__value = self.from_ast(Compiler.get_attr(expression, "value"))

	def transpile(self) -> str:
		"""
		Transpiles the constant to a string.
		"""
		return f"return {self.__value.transpile()};"
