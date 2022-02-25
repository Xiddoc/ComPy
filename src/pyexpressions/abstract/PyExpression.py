"""
PyExpression base class.
Used in extending for other pyexpressions.
"""
from _ast import AST
from abc import abstractmethod, ABCMeta
from typing import Set, Iterable, Optional, TYPE_CHECKING, cast

from src.compiler.Util import Util
from src.scopes.Scope import Scope
from src.structures.Errors import UnsupportedFeatureException
from src.structures.TypeRenames import GENERIC_PYEXPR_TYPE

# If PyExpression is referenced in an import you
# need for type hinting, then add the import here.
# This will ONLY import it when performing type checking,
# therefore no ImportError will occur.
if TYPE_CHECKING:
	from src.pybuiltins.PyPortFunction import PyPortFunction


class PyExpression(metaclass=ABCMeta):
	"""
	PyExpression base class.
	"""

	__expression: AST
	__depends: Set[str]
	__ported_depends: Set["PyPortFunction"]
	__parent: Optional[GENERIC_PYEXPR_TYPE]

	@abstractmethod
	def __init__(self, expression: AST, parent: Optional[GENERIC_PYEXPR_TYPE]):
		"""
		Constructor for the expression.
		"""
		# Create depenency sets
		self.__depends = set()
		# Assign parent node
		self.__parent = parent
		# Local import to avoid error
		self.__ported_depends = set()
		# Create logger for this node
		# Import dependencies locally to avoid import errors
		from src.compiler.Logger import Logger
		from src.compiler.Compiler import Compiler
		self.__logger = Logger(self)
		# Set base expression (might be needed later for throwing errors, will be useful for getting line #)
		self.__expression = expression
		# Print logging statement for creation of node
		self.__logger.log_tree_up(
			f"Creating expression <{Util.get_name(expression)}>: {Compiler.unparse_escaped(expression)} "
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
		self.__logger.log_tree_down(
			f"Compiled <{Util.get_name(self.get_expression())}> expression to: {Util.escape(transpiled_code)}"
		)
		# Return transpilation
		return transpiled_code

	def get_nearest_scope(self) -> Scope:
		"""
		Returns the nearest Scope instance to this instance.
		"""
		# Import locally to avoid cyclical import error
		from src.pyexpressions.concrete.PyFunctionDef import PyFunctionDef
		from src.pyexpressions.concrete.PyModule import PyModule

		# Assign our parent to a temporary variable for iterating
		temp_parent = self.get_parent()

		# Traverse upwards (We could put the condition here,
		# although it causes type hinting bugs which would
		# lead to a lot of unnecessary type casting).
		while True:
			# If we hit a function or module
			if isinstance(temp_parent, PyFunctionDef) or isinstance(temp_parent, PyModule):
				# Get the scope
				return temp_parent.get_scope()
			# Otherwise,
			else:
				# Type cast to bypass type checking bug
				# (Type[MY_CLASS] means MY_CLASS.__class__ and any class that inherits MY_CLASS)
				temp_parent = cast(PyExpression, temp_parent).get_parent()

	def add_dependencies(self, dependencies: Iterable[str]) -> None:
		"""
		Adds multiple dependencies to the dependency list.

		:param dependencies: A list of native dependencies that this object relies on.
		"""
		# If we are on the outer scope
		if self.is_exterior_scope():
			# Then add the dependencies
			self.__depends.update(dependencies)
		# Otherwise,
		else:
			# Recurse upwards (up the parent node, towards the outer scope)
			self.get_parent().add_dependencies(dependencies)

	def get_dependencies(self) -> Set[str]:
		"""
		Returns the list of dependencies that this expression relies on.
		"""
		return self.__depends

	def add_ported_dependency(self, ported_dependency: "PyPortFunction") -> None:
		"""
		Adds a single ported (reimplemented in native language) dependency to the list.

		:param ported_dependency: The ported dependency to add.
		"""
		# If we are on the outer scope
		if self.is_exterior_scope():
			# Then add the dependencies
			self.__ported_depends.add(ported_dependency)
		# Otherwise,
		else:
			# Recurse upwards (up the parent node, towards the outer scope)
			self.get_parent().add_ported_dependency(ported_dependency)

	def add_ported_dependencies(self, ported_dependencies: Iterable["PyPortFunction"]) -> None:
		"""
		Adds multiple ported (reimplemented in native language) dependencies to the dependency list.

		:param ported_dependencies: A list of ported dependencies that this object relies on.
		"""
		# If we are on the outer scope
		if self.is_exterior_scope():
			# Then add the dependencies
			self.__ported_depends.update(ported_dependencies)
		# Otherwise,
		else:
			# Recurse upwards (up the parent node, towards the outer scope)
			self.get_parent().add_ported_dependencies(ported_dependencies)

	def get_ported_dependencies(self) -> Set["PyPortFunction"]:
		"""
		Returns the list of ported dependencies that this expression relies on.
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

	def is_exterior_scope(self) -> bool:
		"""
		:return: Returns True if this is the outer-most scope.
		"""
		return self.get_parent() is None

	def set_expression(self, new_expression: AST) -> None:
		"""
		Updates the current AST node.
		"""
		self.__expression = new_expression

	def from_ast(self, expression: AST) -> "PyExpression":
		"""
		Converts an AST expression to a PyExpression object.

		As opposed to the static from_ast method, this one
		inherits dependencies directly to the current object.

		:param expression: The expression to convert.
		:return: A PyExpression object of the matching type.
		"""
		# Convert to PyExpression and return
		return PyExpression.from_ast_statically(expression, self)

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
