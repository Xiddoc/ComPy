"""
Function defenition.
"""
from _ast import Expr
from typing import List

from src.expressions.PyArg import PyArg
from src.expressions.PyExpression import PyExpression
from src.expressions.PyName import PyName


class PyFunctionDef(PyExpression):
	"""
	Function defenition.
	"""

	__func_name: str
	__args: List[PyArg]
	__code: List[PyExpression]
	__return_type: PyName

	def __init__(self, expression: Expr):
		super().__init__(expression)
		# Convert and store
		self.__func_name = expression.name
		self.__args = [PyArg(arg) for arg in expression.args.args]
		self.__code = [PyExpression.from_ast(ast) for ast in expression.body]
		self.__return_type = PyName(expression.returns)

	def transpile(self) -> str:
		"""
		Transpiles the constant to a string.
		"""
		return f"{self.__return_type.transpile()} {self.__func_name}(" \
		       f"{','.join([arg.transpile() for arg in self.__args])})" \
		       f"{{{''.join([expr.transpile() for expr in self.__code])}}}"
