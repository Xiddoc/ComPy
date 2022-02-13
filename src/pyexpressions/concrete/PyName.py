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
		self.__target = self.translate_builtin_name(expression.id)

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

	@staticmethod
	def translate_builtin_name(object_name: str) -> str:
		"""
		Translates a builtin name to it's native name, if it exists.
		Otherwise, returns the same name.

		:param object_name: The name to translate.
		"""
		from src.compiler.Constants import PY_TYPES_TO_NATIVE_TYPES

		# If we can convert it
		if object_name in PY_TYPES_TO_NATIVE_TYPES:
			# Then use the conversion function
			# to turn it into a string format,
			# where we can inject it into the output native code
			return PY_TYPES_TO_NATIVE_TYPES[object_name]
		else:
			# Otherwise, return the name
			return object_name
