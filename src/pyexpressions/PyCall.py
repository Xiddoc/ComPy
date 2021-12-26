"""
Expression statement.
"""
from _ast import Call
from typing import List

from src.pyexpressions.PyExpression import PyExpression
from src.pyexpressions.PyName import PyName


class PyCall(PyExpression):
	"""
	Expression statement.
	"""

	__args: List[PyExpression]
	__func: PyName

	def __init__(self, expression: Call):
		super().__init__(expression)
		# Convert to name
		self.__func = PyName(expression.func)

		# For each argument
		# Convert to argument object and store
		self.__args = [self.from_ast(arg) for arg in expression.args]

		# Import locally to avoid import error
		from src.pybuiltins.builtins import objs

		# Check if called function is a builtin module
		if self.__func.get_name() in objs:
			# Add as dependency
			self.add_native_dependency(objs[self.__func.get_name()])

	def transpile(self) -> str:
		"""
		Transpiles the constant to a string.
		"""
		# Transpile the actual function call to the matching native code...
		# Take function name
		# Add parenthesis
		# For each argument, transpile
		# Join the arguments together with commas
		# FUNC_NAME ( ARG1 , ARG2 , ... )
		return f"{self.__func.transpile()}({','.join([arg.transpile() for arg in self.__args])})"
