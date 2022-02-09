"""
Constant literal.
"""
from _ast import Constant
from typing import Type, Any

from src.pyexpressions.abstract.PyExpression import PyExpression
from src.structures.Errors import UnsupportedFeatureException
from src.structures.TypeRenames import GENERIC_PYEXPR_TYPE


class PyConstant(PyExpression):
	"""
	Literal constant value.
	"""

	__value: str

	def __init__(self, expression: Constant, parent: GENERIC_PYEXPR_TYPE):
		super().__init__(expression, parent)
		# Translate the value
		self.__value = self.translate_constant(expression)

	def _transpile(self) -> str:
		"""
		Transpiles the constant to a string.
		"""
		return self.__value

	@staticmethod
	def translate_constant(constant: Constant) -> str:
		"""
		Transpiles a constant to it's string representation.
		:param constant: The Constant object to transpile.
		"""
		# Get the constant's value
		constant_value: Any = constant.value

		# Get the contant's value type
		value_type: Type[Any] = type(constant_value)

