"""
Name statement (usage of an object).
"""
from _ast import Name

from src.expressions.PyExpression import PyExpression


class PyName(PyExpression):
	"""
	Name statement (usage of an object).
	"""

	__target: str

	def __init__(self, expression: Name):
		super().__init__(expression)
		# Store the variable name
		self.__target = expression.id

	def transpile(self) -> str:
		"""
		Transpiles the constant to a string.
		"""
		return self.__target
