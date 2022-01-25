"""
Port a native function or object to Python.
"""
from typing import Any, Iterable, Optional, Set

from src.pyexpressions.PyExpression import PyExpression
from src.structures.TypeRenames import AnyFunction


class PyPortFunction(PyExpression):
	"""
	Port a native function or object to Python.
	"""

	# __func has a type of PyFunctionDef, but you
	# can't specify it here without a circular import
	# error so we will (overwrite) type hint in the constructor instead.
	__func: Any
	# Native code as a string
	__code: str
	# A list of native dependencies
	__native_depends: Set[str]

	def __init__(self, function: AnyFunction, code: str, dependencies: Optional[Iterable[str]] = None):
		# Create a new set if there are no dependencies passed, otherwise use the passed dependencies
		super().__init__(None, None)

		# Import locally so that PyExpression can use this directly
		from src.pyexpressions.PyFunctionDef import PyFunctionDef
		# Convert the function to a PyFunctionDef that can be represented locally later (as function header)
		self.__func: PyFunctionDef = PyFunctionDef.from_single_object(function, self)
		# Store the native code segment
		self.__code = code

		# Initialize the dependency set
		self.__native_depends = set()
		# If there are any dependencies
		if dependencies is not None:
			# Add them as an iterable
			self.add_native_dependencies(dependencies)

	def add_native_dependencies(self, native_dependencies: Iterable[str]) -> None:
		"""
		Adds multiple native dependencies to the dependency list.

		:param native_dependencies: A list of native dependencies that this object relies on.
		"""
		self.__native_depends.update(native_dependencies)

	def _transpile(self) -> str:
		"""
		Transpile the ported function to an entirely native function.
		"""
		return f"{self.__func.transpile_header()}{{{self.__code}}}"
