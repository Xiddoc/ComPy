"""
Function defenition.
"""
from _ast import FunctionDef, Constant
from ast import parse
from inspect import getsource
from typing import List, cast, Optional, Any

from src.compiler.Util import Util
from src.pyexpressions.abstract.PyExpression import PyExpression
from src.pyexpressions.concrete.PyArg import PyArg
from src.pyexpressions.concrete.PyName import PyName
from src.pyexpressions.highlevel.PyBody import PyBody
from src.pyexpressions.highlevel.PyIdentifiable import PyIdentifiable
from src.pyexpressions.highlevel.PyScoped import PyScoped
from src.scopes.objects.Type import Type
from src.scopes.objects.Function import Function
from src.scopes.objects.Variable import Variable
from src.structures.TypeRenames import GENERIC_PYEXPR_TYPE, AnyFunction


class PyFunctionDef(PyScoped, PyIdentifiable):
	"""
	Function defenition.
	"""

	__args: List[PyArg]
	__defaults: List[PyExpression]
	__code: PyBody
	__return_type: Optional[PyName]

	def __init__(self, expression: FunctionDef, parent: GENERIC_PYEXPR_TYPE):
		super().__init__(expression, parent)
		from src.pybuiltins.PyPortFunction import PyPortFunction

		# Convert and store
		self.set_id(expression.name)

		# If return is a Constant, then it is None (there is no return value)
		# In which case in the transpilation stage, set as "void"
		# Otherwise, use a proper name (int, str, etc.)
		returns = Util.get_attr(expression, 'returns')
		self.__return_type = None if isinstance(returns, Constant) else PyName(returns, self)

		# If this is not a ported object (we will handle duplicated objects externally using a set)
		if not isinstance(parent, PyPortFunction):
			# Create a function scope signature
			scope_sig = Function(name=self.get_id(), return_type=Type(returns.id if self.__return_type else 'NoneType'))
			# Add this function to the nearest scope
			self.get_nearest_scope().declare_object(scope_sig)

		# Create object scope (function body has it's own scope)
		# Inherit the scope from the previous scope
		self.update_from_nearest_scope()

		# For each function argument
		self.__args = []
		for arg in expression.args.args:
			# If this is a constructor self-reference ('self' argument)
			# Create current argument
			new_arg = PyArg(arg, self)

			# Create scope signature for argument
			arg_scope_sig = Variable(name=new_arg.get_id(), type=Type(new_arg.get_type().get_id()))
			# Assign all stack variables to our scope
			self.get_scope().declare_object(arg_scope_sig)

			# If this is not the "self" argument
			if not new_arg.is_self_arg():
				# Add to argument list
				# A few lines up, we DO define it in the scope, since it might be referenced.
				# However, we don't want to transpile it, since C++ does not use it for function arguments.
				self.__args.append(new_arg)

		# For each argument default
		# In my opinion, this should be moved to the PyArg class, however
		# for the sake of compatibility (maybe AST will change their class
		# model in the future) I will implement it similar to the AST class-
		# default values will go in the "Function Definition" AST node.
		self.__defaults = [self.from_ast(default) for default in expression.args.defaults]

		# For each line of code, convert to expression
		self.__code = PyBody(expression.body, self)

	def transpile_code(self) -> str:
		"""
		Transpile the code body of the function.
		"""
		return self.__code.transpile()

	# noinspection PyUnusedFunction
	def _transpile(self) -> str:
		"""
		Transpile the statement to a string.
		"""
		# Join the header and the body together
		return f"{self.transpile_header()} {self.transpile_code()}"

	def transpile_return_type(self) -> str:
		"""
		Transpiles the return type of the function to a native string.
		"""
		return self.__return_type.transpile() if self.__return_type else 'void'

	def transpile_args(self) -> str:
		"""
		Transpiles the arguments of the function and merges them together.
		"""
		# Transpile the arguments
		transpiled_arguments: List[str] = []

		#   def func(arg1, arg2, arg3 = 1, arg4 = 2)
		#      ARGS [ - - - - - - - - - - - - - - -]
		#  DEFAULTS              [ - - - - - - - - ]

		# For each argument without a default
		non_default_count = len(self.__args) - len(self.__defaults)
		for i in range(non_default_count):
			# Transpile it and add it to the list
			transpiled_arguments.append(self.__args[i].transpile())

		# Take the defaulted arguments from the end of __args
		for i, j in zip(range(non_default_count, len(self.__args)), range(len(self.__defaults))):
			# Transpile each argument, merge it with the default value, then add it to the list.
			transpiled_arguments.append(f"{self.__args[i].transpile()} = {self.__defaults[j].transpile()}")

		# Merge them together with commas
		return ', '.join(transpiled_arguments)

	def transpile_header(self) -> str:
		"""
		Transpiles the header of the function to a native string.
		"""
		# Transpile the return type, then merge it with
		# the function name and transpiled arguments.
		return f"{self.transpile_return_type()} {self.get_id()}({self.transpile_args()})"

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
		return hash(self.get_id())
