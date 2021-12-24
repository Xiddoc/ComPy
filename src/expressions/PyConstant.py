"""
Constant literal.
"""
from _ast import Constant
from json import dumps

from src.Errors import UnsupportedFeatureException
from src.expressions.PyExpression import PyExpression


class PyConstant(PyExpression):
	"""
	Literal constant value.
	"""

	__value: str

	def __init__(self, expression: Constant):
		super().__init__(expression)
		# Translate the value
		self.__value = self.translate_constant(expression)

	def transpile(self) -> str:
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
		# Get the contant's value type
		value_type = type(constant.value)
		# If the type is an integer or a boolean
		if value_type == int or value_type == bool:
			# Return the value
			return str(constant.value)

		elif value_type == str:
			# Encompass in quotes
			return dumps(constant.value)

		else:
			# What type is that?
			# We can't use that
			raise UnsupportedFeatureException(f"Python type '{value_type}' is not supported by the compiler.")
