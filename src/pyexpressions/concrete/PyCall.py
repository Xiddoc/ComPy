"""
Call a function.
"""
from _ast import Call
from typing import List

from src.compiler.Compiler import Compiler
from src.pybuiltins.PyPortFunction import PyPortFunction
from src.pyexpressions.abstract.PyExpression import PyExpression
from src.pyexpressions.concrete.PyName import PyName
from src.structures.TypeRenames import GENERIC_PYEXPR_TYPE


class PyCall(PyExpression):
	"""
	Call a function.
	"""

	__args: List[PyExpression]
	__func: PyName

	def __init__(self, expression: Call, parent: GENERIC_PYEXPR_TYPE):
		super().__init__(expression, parent)
		# Convert to name
		self.__func = PyName(Compiler.get_attr(expression, 'func'), self)

		# For each argument
		# Convert to argument object and store
		self.__args = [self.from_ast(arg) for arg in expression.args]

		# Import locally to avoid import error
		from src.pybuiltins.builtins import objs

		# Check if called function is a builtin module
		if self.__func.get_name() in objs:
			# Get function
			native_func: PyPortFunction = PyPortFunction(objs[self.__func.get_name()], self)
			# Inherit dependencies
			self.add_dependencies(native_func.get_dependencies())
			# Add as dependency
			self.add_ported_dependency(native_func)

	def _transpile(self) -> str:
		"""
		Transpile the operation to a string.
		"""
		# Transpile the actual function call to the matching native code...
		# Take function name
		# Add parenthesis
		# For each argument, transpile
		# Join the arguments together with commas
		# FUNC_NAME ( ARG1 , ARG2 , ... )
		return f"{self.__func.transpile()}({','.join([arg.transpile() for arg in self.__args])});"