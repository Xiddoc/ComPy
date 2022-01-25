"""
PyExpression base class.
Used in extending for other pyexpressions.
"""
from _ast import AST
from abc import abstractmethod, ABCMeta
from typing import Set, Iterable, Optional, Any, cast

from src.compiler.Args import Args
from src.scopes.Scope import Scope
from src.structures.Errors import UnsupportedFeatureException
from src.structures.TypeRenames import GENERIC_PYEXPR_TYPE


class PyExpression(metaclass=ABCMeta):
	"""
	PyExpression base class.
	"""

	__expression: AST
	__depends: Set[str]
	__ported_depends: Set[Any]
	__parent: Optional[GENERIC_PYEXPR_TYPE]

	@abstractmethod
	def __init__(self, expression: Optional[AST], parent: Optional[GENERIC_PYEXPR_TYPE]):
		"""
		Constructor for the expression.
		"""
		# Set base expression (might be needed later for throwing errors, will be useful for getting line #)
		self.__expression = expression
		# Create depenency sets
		self.__depends = set()
		# Assign parent node
		self.__parent = parent
		# Local import to avoid error
		from src.pybuiltins.PyPortFunction import PyPortFunction
		self.__ported_depends = cast(Set[PyPortFunction], set())
		# Create logger for this node
		# Import dependencies locally to avoid import errors
		from src.compiler.Logger import Logger
		from src.compiler.Compiler import Compiler
		self.__logger = Logger(self)
		# Print logging statement for creation of node
		self.__logger.log_tree_up(
			f"Creating expression <{Compiler.get_name(expression)}>: "
			f"{'<Native Object>' if expression is None else Compiler.unparse_escaped(expression)} "
		)

	@abstractmethod
	def _transpile(self) -> str:
		"""
		Transpiles this expression to a C++ string.

		This is the *wrapped* method. We (the devs) will use this method
		to *IMPLEMENT* the transpilation process. To actually transpile
		the code, use the self.transpile method, which wraps this method.
		"""

	def transpile(self) -> str:
		"""
		Transpiles this expression to a C++ string.

		This is the *wrapper* method. We (the devs) will use this
		method to *EXECUTE* the transpilation process. To actually
		implement the transpilation process, implement the
		self._transpile method, which is wrapped by this method.
		"""
		# Execute the transpilation process by executing
		# the *IMPLEMENTATION* of the transpiler function
		transpiled_code: str = self._transpile()
		# Currently, the only wrapping that we will do is logging.
		# However, this still allows for future useful extensions
		# such as beautifying the code, for example.
		from src.compiler.Compiler import Compiler
		self.__logger.log_tree_down(
			f"Compiled <{Compiler.get_name(self.get_expression())}> expression to: {transpiled_code}")
		# Return the transpiled code (with a comment, if it is enabled)
		return \
			f"/* {Compiler.unparse_escaped(self.get_expression())} */ {transpiled_code}" \
			if Args().get_args().comment else \
			transpiled_code

	def get_nearest_scope(self) -> Scope:
		"""
		Returns the nearest Scope instance to this instance.
		"""
		# Import locally to avoid cyclical import error
		from src.pyexpressions.PyFunctionDef import PyFunctionDef

		# Assign our parent to a temporary variable for iterating
		temp_parent = self.get_parent()

		# Traverse upwards
		while True:
			# TODO: Change this to 'or' statement after Compiler scope implemented
			# If we hit a function scope
			if isinstance(temp_parent, PyFunctionDef):
				# Declare the variable
				return temp_parent.get_scope()
			# If we hit the head scope (Compiler scope / module layer)
			elif temp_parent is None:
				# break
				return Scope()
			# Otherwise,
			else:
				# Traverse to next parent
				temp_parent = temp_parent.get_parent()

	def add_dependencies(self, dependencies: Iterable[str]) -> None:
		"""
		Adds multiple dependencies to the dependency list.

		:param dependencies: A list of native dependencies that this object relies on.
		"""
		self.__depends.update(dependencies)

	def get_dependencies(self) -> Set[str]:
		"""
		Returns the list of dependencies that this expression relies on.
		"""
		return self.__depends

	def add_ported_dependencies(self, ported_dependencies: Iterable[Any]) -> None:
		"""
		Adds multiple ported (reimplemented in native language) dependencies to the dependency list.

		:param ported_dependencies: A list of native dependencies that this object relies on.
		"""
		from src.pybuiltins.PyPortFunction import PyPortFunction
		self.__ported_depends.update(cast(Iterable[PyPortFunction], ported_dependencies))

	def get_ported_dependencies(self) -> Set[Any]:
		"""
		Returns the list of native (ported) dependencies that this expression relies on.
		"""
		return self.__ported_depends

	def get_expression(self) -> AST:
		"""
		:return: Returns the expression this instance is holding (was initialized with).
		"""
		return self.__expression

	def get_parent(self) -> Optional[GENERIC_PYEXPR_TYPE]:
		"""
		:return: Returns an instance of the PyExpression object which created this object.
		"""
		return self.__parent

	def from_ast(self, expression: AST) -> "PyExpression":
		"""
		Converts an AST expression to a PyExpression object.

		As opposed to the static from_ast method, this one
		inherits dependencies directly to the current object.

		:param expression: The expression to convert.
		:return: A PyExpression object of the matching type.
		"""
		# Convert to PyExpression
		obj: PyExpression = PyExpression.from_ast_statically(expression, self)
		# Inherit / extend dependencies to this object
		self.add_dependencies(obj.get_dependencies())
		self.add_ported_dependencies(obj.get_ported_dependencies())
		# Return new object
		return obj

	@staticmethod
	def from_ast_statically(expression: AST, parent: Optional[GENERIC_PYEXPR_TYPE]) -> "PyExpression":
		"""
		Converts an AST expression to a PyExpression object.

		:param expression: The expression to convert.
		:param parent: The parent expression which uses this node.
		:return: A PyExpression object of the matching type.
		"""
		# Local import to avoid circular import errors
		from src.compiler.Constants import AST_EXPR_TO_PYEXPR

		# Get the expression type
		expr_type = type(expression)

		# If the expression is valid
		if expr_type in AST_EXPR_TO_PYEXPR:
			# Convert to PyExpression and return
			return AST_EXPR_TO_PYEXPR[expr_type](expression, parent)
		# Otherwise, it is probably a feature we do not support
		else:
			raise UnsupportedFeatureException(expression)
