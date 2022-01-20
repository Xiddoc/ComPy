"""
Name statement (usage of an object).
"""
from _ast import Name

from src.pyexpressions.PyExpression import PyExpression


class PyName(PyExpression):
	"""
	Name statement (usage of an object).
	"""

	__target: str

	def __init__(self, expression: Name):
		super().__init__(expression)
		# Store the variable name
		self.__target = expression.id

	def get_name(self) -> str:
		"""
		Return the name of the object.
		"""
		return self.__target

	def transpile(self) -> str:
		"""
		Transpiles the constant to a string.
		"""
		return self.__target