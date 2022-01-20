"""
Return statement.
"""
from _ast import Return

from src.Compiler import Compiler
from src.TypeRenames import GENERIC_PYEXPR_TYPE
from src.pyexpressions.PyExpression import PyExpression


class PyReturn(PyExpression):
	"""
	Return statement.
	"""

	__value: PyExpression

	def __init__(self, expression: Return, parent: GENERIC_PYEXPR_TYPE):
		super().__init__(expression, parent)
		# Translate the value
		self.__value = self.from_ast(Compiler.get_attr(expression, "value"))

	def transpile(self) -> str:
		"""
		Transpiles the constant to a string.
		"""
		return f"return {self.__value.transpile()};"
