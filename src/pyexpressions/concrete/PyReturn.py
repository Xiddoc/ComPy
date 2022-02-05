"""
Return statement.
"""
from _ast import Return

from src.compiler.Compiler import Compiler
from src.compiler.Util import Util
from src.pyexpressions.abstract.PyExpression import PyExpression
from src.structures.TypeRenames import GENERIC_PYEXPR_TYPE


class PyReturn(PyExpression):
	"""
	Return statement.
	"""

	__value: PyExpression

	def __init__(self, expression: Return, parent: GENERIC_PYEXPR_TYPE):
		super().__init__(expression, parent)
		# Translate the value
		self.__value = self.from_ast(Util.get_attr(expression, "value"))

	def _transpile(self) -> str:
		"""
		Transpiles the constant to a string.
		"""
		return f"return {self.__value.transpile()};"
