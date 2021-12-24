"""
Function argument name declaration.
"""
from _ast import arg

from src.expressions.PyExpression import PyExpression
from src.expressions.PyName import PyName


class PyArg(PyExpression):
	"""
	Function argument name declaration.
	"""

	__arg_name: str
	__arg_type: PyName

	def __init__(self, expression: arg):
		super().__init__(expression)
		# Convert and store
		self.__arg_name = expression.arg
		self.__arg_type = PyName(expression.annotation)

	def transpile(self) -> str:
		"""
		Transpiles the constant to a string.
		"""
		return f"{self.__arg_type.transpile()} {self.__arg_name}"
