"""
Port a native function or object to Python.
"""
from typing import Any, Iterable, Optional

from src.TypeRenames import AnyFunction
from src.pybuiltins.PyPort import PyPort


class PyPortFunction(PyPort):
	"""
	Port a native function or object to Python.
	"""

	# __func has a type of PyFunctionDef, but you
	# can't specify it here without a circular import
	# error so we will (overwrite) type hint in the constructor instead.
	__func: Any
	__code: str

	def __init__(self, function: AnyFunction, code: str, dependencies: Optional[Iterable[str]] = None):
		# Create a new set if there are no dependencies passed, otherwise use the passed dependencies
		super().__init__(set() if dependencies is None else set(dependencies))

		# Import locally so that PyExpression can use this directly
		from src.pyexpressions.PyFunctionDef import PyFunctionDef

		# Convert the function to a PyFunctionDef that can be represented locally later (as function header)
		self.__func: PyFunctionDef = PyFunctionDef.from_single_object(function, self)

		# Store the native code segment
		self.__code = code

	def transpile(self) -> str:
		"""
		Transpile the ported function to an entirely native function.
		"""
		return f"{self.__func.transpile_header()}{{{self.__code}}}"
