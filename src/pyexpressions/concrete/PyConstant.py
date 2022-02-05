"""
Constant literal.
"""
from _ast import Constant
from json import dumps
from typing import Type, Union

from src.compiler.Util import Util
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
		val: Union[int, str, bool] = Util.get_attr(constant, 'value')

		# Get the contant's value type
		value_type: Type[Union[int, str, bool]] = type(val)

		# If the type is an integer or a boolean
		if value_type == int or value_type == bool:
			# Return the value
			return str(val)

		elif value_type == str:
			# Encompass in quotes
			return dumps(val)

		else:
			# What type is that?
			# We can't use that
			raise UnsupportedFeatureException(constant)
