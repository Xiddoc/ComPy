"""
Port a native function or object to Python.
"""
from typing import Any, Set


class PyPort:
	"""
	Port a native function or object to Python.
	"""

	__func: Any
	__code: str

	def __init__(self, obj: Any, code: str, dependencies: Set[str] = None):
		"""
		@param obj: The object to port.
		@param code: The native code for the function.
		@param dependencies: A list of dependencies to require.
		"""
		# Import locally so that PyExpression can use this directly
		from src.pyexpressions.PyFunctionDef import PyFunctionDef

		# Convert the object to an expression that can be represented locally
		self.__func: PyFunctionDef = PyFunctionDef.from_single_object(obj)

		# Store the native code segment
		self.__code = code
		# Optional parameter
		if dependencies is None:
			# Use immutable object for "default" value
			dependencies = set()

	def transpile(self) -> str:
		"""
		Transpile the ported function to an entirely native function.
		"""
		return f"{self.__func.transpile_header()}{{{self.__code}}}"
