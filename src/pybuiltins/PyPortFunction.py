"""
Port a native function or object to Python.
"""
from typing import Iterable, Set, Any

from src.pybuiltins.PyPortFunctionSignature import PyPortFunctionSignature
from src.pyexpressions.PyExpression import PyExpression
from src.pyexpressions.PyFunctionDef import PyFunctionDef
from src.structures.TypeRenames import GENERIC_PYEXPR_TYPE


class PyPortFunction(PyExpression):
	"""
	Port a native function or object to Python.
	"""

	# __func has a type of PyFunctionDef, but you
	# can't specify it here without a circular import
	# error so we will (overwrite) type hint in the constructor instead.
	__func: PyFunctionDef
	# Native code as a string
	__code: str
	# A list of native dependencies
	__native_depends: Set[str]

	def __init__(self, func_sig: PyPortFunctionSignature, parent: GENERIC_PYEXPR_TYPE):
		"""
		Initializes the ported function using a loaded signature.

		:param func_sig: The function signature and body.
		:param parent: The parent node to this expression.
		"""
		# There is no expression (this node does not exist in the given Python code)
		# Pass the parent node
		super().__init__(self, parent)

		# Convert the function to a PyFunctionDef that can be represented locally later (as function header)
		self.__func: PyFunctionDef = PyFunctionDef.from_single_object(func_sig.function, self)
		# Store the native code segment
		self.__code = func_sig.code

		# Initialize the dependency set
		self.__native_depends = set()
		# If there are any dependencies
		if func_sig.dependencies is not None:
			# Add them as an iterable
			self.add_native_dependencies(func_sig.dependencies)

	def add_native_dependencies(self, native_dependencies: Iterable[str]) -> None:
		"""
		Adds multiple native dependencies to the dependency list.

		:param native_dependencies: A list of native dependencies that this object relies on.
		"""
		self.__native_depends.update(native_dependencies)

	def get_native_dependencies(self) -> Set[str]:
		"""
		Returns the set of native dependencies that this port relies on.
		"""
		return self.__native_depends

	def _transpile(self) -> str:
		"""
		Transpile the ported function to an entirely native function.
		"""
		return f"{self.__func.transpile_header()}{{{self.__code}}}"

	def __eq__(self, other: Any) -> bool:
		return isinstance(other, PyPortFunction) and hash(self) == hash(other)

	def __hash__(self) -> int:
		return hash(self.__func)
