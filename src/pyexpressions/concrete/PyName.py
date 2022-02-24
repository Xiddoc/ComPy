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
		# Import locally to avoid import error
		from src.pyexpressions.concrete.PyCall import PyCall
		from src.pybuiltins.PyPortManager import PyPortManager

		# Store the object name to a class variable
		# If this was used in a PyCall, then don't try to
		# convert it since it's not a type, it's a function.
		# For example:
		# first_var: str = "Hello"  # Name used as type annotation
		# second_var = str(10)  # Name used as type conversion/cast function
		if isinstance(parent, PyCall):
			# Check if this is a ported and linked object
			if PyPortManager().is_loaded(expression.id):
				# Then retrieve it from the manager
				# Update target name (we will use the native function name)
				self.__target = PyPortManager().call_port(expression.id, self).get_func_name()
			else:
				# Otherwise, use the function name directly.
				# This line should be equivalent to using expression.id
				# directly, although the Scope handler will throw an
				# error if it can't retrieve the object (it does not exist).
				self.__target = self.get_nearest_scope().get_object(expression.id).name
		else:
			# Otherwise, translate it as a type hint
			self.__target = self.translate_builtin_name(expression.id)

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
