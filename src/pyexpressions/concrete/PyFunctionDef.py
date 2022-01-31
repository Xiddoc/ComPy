"""
Function defenition.
"""
from _ast import FunctionDef, Constant
from ast import parse
from inspect import getsource
from typing import List, cast, Optional, Any

from src.pyexpressions.concrete.PyArg import PyArg
from src.pyexpressions.abstract.PyExpression import PyExpression
from src.pyexpressions.concrete.PyName import PyName
from src.scopes.Scope import Scope
from src.structures.TypeRenames import GENERIC_PYEXPR_TYPE, AnyFunction


class PyFunctionDef(PyExpression):
	"""
	Function defenition.
	"""

	__func_name: str
	__args: List[PyArg]
	__code: List[PyExpression]
	__return_type: Optional[PyName]
	__scope: Scope

	def __init__(self, expression: FunctionDef, parent: GENERIC_PYEXPR_TYPE):
		super().__init__(expression, parent)
		# Convert and store
		self.__func_name = expression.name
		# Create object scope (function body has it's own scope)
		self.__scope = Scope(self.get_nearest_scope())
		# For each function argument
		# Convert to argument
		self.__args = [PyArg(arg, self) for arg in expression.args.args]
		# For each line of code, convert to expression
		self.__code = [self.from_ast(ast) for ast in expression.body]
		# If return is a Constant, then it is None (there is no return value)
		# In which case in the transpilation stage, set as "void"
		# Otherwise, use a proper name (int, str, etc.)
		from src.compiler.Compiler import Compiler
		returns = Compiler.get_attr(expression, 'returns')
		self.__return_type = None if type(returns) == Constant else PyName(returns, self)

	def _transpile(self) -> str:
		"""
		Transpile the operation to a string.
		"""
		return f"{self.transpile_header()}{{{''.join([expr.transpile() for expr in self.__code])}}}"

	def transpile_header(self) -> str:
		"""
		Transpiles the header of the function to a native string.
		"""
		return f"{self.__return_type.transpile() if self.__return_type else 'void'}" \
		       f" {self.__func_name}(" \
		       f"{','.join([arg.transpile() for arg in self.__args])})"

	# noinspection PyUnusedFunction
	def get_scope(self) -> Scope:
		"""
		Returns the Scope (instance) of this function body.

		Might have a warning in your IDE that labels it as "unused".
		This is since it is not explicitly used (in PyExpression:
		it *should* be casted to PyFunctionDef, then use obj.get_scope(),
		but instead there is a type check, then we use get_scope.

		What this means is that depending on the Python linter
		implementation, your IDE could flag this function as useless.
		It is not. Do **NOT** remove it.
		"""
		return self.__scope

	@staticmethod
	def from_single_object(obj: AnyFunction, parent: Optional[GENERIC_PYEXPR_TYPE]) -> "PyFunctionDef":
		"""
		Converts any singular (function, object, class, etc.) Python object to an AST node.

		:param obj: The object to convert.
		:param parent: The parent expression which uses this node.
		:return: The parsed AST node.
		"""
		# Get the source code of the object
		# Parse it to an AST tree
		# Get the body of the AST tree (scope is Module)
		# Get the first line
		# Turn it into a PyExpression
		py_expr: PyExpression = PyExpression.from_ast_statically(
			expression=parse(getsource(obj)).body[0],
			parent=parent
		)

		# Cast it to new type
		py_def: "PyFunctionDef" = cast("PyFunctionDef", py_expr)

		# Return the casted expression object
		return py_def

	def __eq__(self, other: Any) -> bool:
		return isinstance(other, PyFunctionDef) and hash(self) == hash(other)

	def __hash__(self) -> int:
		return hash(self.__func_name)