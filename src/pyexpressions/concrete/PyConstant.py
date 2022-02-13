"""
Constant literal.
"""
from _ast import Constant
from typing import Any

from src.compiler.Util import Util
from src.pyexpressions.abstract.PyExpression import PyExpression
from src.scopes.Type import Type
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

		# Get the contant's type
		# Then, get the name of the type
		# Try to look up the conversion function
		# Then, call the function using the value itself
		return Type.type_name_to_conversion_func(Util.get_name(constant_value))(constant_value)
