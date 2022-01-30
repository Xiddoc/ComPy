"""
Name statement (usage of an object).
"""
from _ast import Name

from src.pyexpressions.abstract.PyExpression import PyExpression
from src.structures.TypeRenames import GENERIC_PYEXPR_TYPE


class PyName(PyExpression):
	"""
	Name statement (usage of an object).
	"""

	__target: str

	def __init__(self, expression: Name, parent: GENERIC_PYEXPR_TYPE):
		super().__init__(expression, parent)
		# Store the variable name
		self.__target = expression.id

	def get_name(self) -> str:
		"""
		Return the name of the object.
		"""
		return self.__target

	def _transpile(self) -> str:
		"""
		Transpiles the constant to a string.
		"""
		return self.__target
