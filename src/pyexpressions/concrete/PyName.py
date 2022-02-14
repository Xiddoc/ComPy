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
		from src.pybuiltins.PyPortFunction import PyPortFunction
		from src.pybuiltins.builtins import objs

		# Store the object name to a class variable
		# If this was used in a PyCall, then don't try to convert it (it's not a type, it's a function)
		if isinstance(parent, PyCall):
			# Set it directly
			self.__target = expression.id

			# Check if called function is a builtin module
			if self.__target in objs:
				# Compile the function to a PyPortFunction expression/object
				native_func: PyPortFunction = PyPortFunction(objs[self.__target], self)
				# Update target name (we will use the native function name)
				self.__target = native_func.get_func_name()

				# Inherit dependencies
				self.add_dependencies(native_func.get_dependencies())
				# Add as dependency
				self.add_ported_dependency(native_func)
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
