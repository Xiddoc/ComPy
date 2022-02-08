"""
Return statement.
"""
from _ast import Return
from typing import Optional

from src.compiler.Util import Util
from src.pyexpressions.abstract.PyExpression import PyExpression
from src.structures.TypeRenames import GENERIC_PYEXPR_TYPE


class PyReturn(PyExpression):
	"""
	Return statement.
	"""

	__value: Optional[PyExpression]

	def __init__(self, expression: Return, parent: GENERIC_PYEXPR_TYPE):
		super().__init__(expression, parent)
		# Translate the value
		# (If none, then set none)
		self.__value = None if expression.value is None else self.from_ast(expression.value)

	def _transpile(self) -> str:
		"""
		Transpiles the constant to a string.
		"""
		# If there is no return value, then just return
		# If there is, then transpile it.
		return "return;" if self.__value is None else f"return {self.__value.transpile()};"
