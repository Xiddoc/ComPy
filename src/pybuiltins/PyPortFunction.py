"""
Port a native function or object to Python.
"""
from ast import Pass
from typing import Any

from src.pybuiltins.PyPortFunctionSignature import PyPortFunctionSignature
from src.pyexpressions.abstract.PyExpression import PyExpression
from src.pyexpressions.concrete.PyFunctionDef import PyFunctionDef
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

	def __init__(self, func_sig: PyPortFunctionSignature, parent: GENERIC_PYEXPR_TYPE):
		"""
		Initializes the ported function using a loaded signature.

		:param func_sig: The function signature and body.
		:param parent: The parent node to this expression.
		"""
		# Pass a "pass" Python AST expression (null operation), explanation a few lines down
		# Pass the parent node as well (us)
		super().__init__(Pass(), parent)

		# Convert the function to a PyFunctionDef that can be represented locally later (as function header)
		self.__func: PyFunctionDef = PyFunctionDef.from_single_object(func_sig.func, self)

		# Set our expression to the FunctionDef AST expression
		# We do this now instead of during the super since we must
		# call super() before running the from_single_object method.
		self.set_expression(self.__func.get_expression())

		# Store the native code segment
		self.__code = func_sig.code

		# If there are any dependencies
		if func_sig.dependencies is not None:
			# Add them as an iterable
			self.add_dependencies(func_sig.dependencies)

		# Finally, add ourselves as a native dependency
		self.add_ported_dependency(self)

	def get_interface_function(self) -> PyFunctionDef:
		"""
		:return: The PyFunctionDef instance which represents how
				the native function is represented in Python. This
				means that the expression instance will look as
				if the function was originally written in Python.
		"""
		return self.__func

	def get_function_name(self) -> str:
		"""
		:return: The native name of the ported function.
		"""
		return self.get_interface_function().get_id()

	def _transpile(self) -> str:
		"""
		Transpile the ported function to an entirely native function.
		"""
		return f"{self.__func.transpile_header()} {{\n{self.__code}\n}}"

	def __eq__(self, other: Any) -> bool:
		return isinstance(other, PyPortFunction) and hash(self) == hash(other)

	def __hash__(self) -> int:
		return hash(self.__func)
