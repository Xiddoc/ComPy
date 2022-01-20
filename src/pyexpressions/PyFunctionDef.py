"""
Function defenition.
"""
from _ast import FunctionDef, Constant
from ast import parse
from inspect import getsource
from typing import List, Union, Callable, Any, cast

from src.Compiler import Compiler
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
		returns = Compiler.get_attr(expression, 'returns')
		self.__return_type = None if type(returns) == Constant else PyName(returns)

	def transpile(self) -> str:
		"""
		Transpiles the constant to a native string.
		"""
		return f"{self.transpile_header()}{{{''.join([expr.transpile() for expr in self.__code])}}}"

	def transpile_header(self) -> str:
		"""
		Transpiles the header of the function to a native string.
		"""
		return f"{self.__return_type.transpile() if self.__return_type else 'void'}" \
		       f" {self.__func_name}(" \
		       f"{','.join([arg.transpile() for arg in self.__args])})"

	@staticmethod
	def from_single_object(obj: Callable[..., Any]) -> "PyFunctionDef":
		"""
		Converts any singular (function, object, class, etc.) Python object to an AST node.

		@param obj: The object to convert.
		@return: The parsed AST node.
		"""
		# Get the source code of the object
		# Parse it to an AST tree
		# Get the body of the AST tree (scope is Module)
		# Get the first line
		# Turn it into a PyExpression
		py_expr: PyExpression = PyExpression.from_ast_statically(parse(getsource(obj)).body[0])

		# Cast it to new type
		py_def: "PyFunctionDef" = cast("PyFunctionDef", py_expr)

		# Return the casted expression object
		return py_def
