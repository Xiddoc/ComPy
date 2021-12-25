"""
Function defenition.
"""
from _ast import FunctionDef, Constant
from typing import List, Union

from src.pyexpressions.PyArg import PyArg
from src.pyexpressions.PyExpression import PyExpression
from src.pyexpressions.PyName import PyName


class PyFunctionDef(PyExpression):
	"""
	Function defenition.
	"""

	__func_name: str
	__args: List[PyArg]
	__code: List[PyExpression]
	__return_type: Union[PyName, None]

	def __init__(self, expression: FunctionDef):
		super().__init__(expression)
		# Convert and store
		self.__func_name = expression.name
		# For each function argument
		# Convert to argument
		self.__args = [PyArg(arg) for arg in expression.args.args]
		# For each line of code, convert to expression
		self.__code = [self.from_ast(ast) for ast in expression.body]
		# If return is a Constant, then it is None (there is no return value)
		# In which case in the transpilation stage, set as "void"
		# Otherwise, use a proper name (int, str, etc.)
		self.__return_type = None if type(expression.returns) == Constant else PyName(expression.returns)

	def transpile(self) -> str:
		"""
		Transpiles the constant to a string.
		"""
		return f"{self.__return_type.transpile() if self.__return_type else 'void'}" \
		       f" {self.__func_name}(" \
		       f"{','.join([arg.transpile() for arg in self.__args])})" \
		       f"{{{''.join([expr.transpile() for expr in self.__code])}}}"
