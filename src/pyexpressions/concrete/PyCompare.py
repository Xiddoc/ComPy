"""
Comparison expression (condition).
"""
from _ast import Compare, cmpop

from src.compiler.Compiler import Compiler
from src.pyexpressions.abstract.PyExpression import PyExpression
from src.structures.Errors import UnsupportedFeatureException
from src.structures.TypeRenames import GENERIC_PYEXPR_TYPE


class PyCompare(PyExpression):
	"""
	Comparison expression (condition).
	"""

	__comparator: str
	__left: PyExpression
	__right: PyExpression

	def __init__(self, expression: Compare, parent: GENERIC_PYEXPR_TYPE):
		super().__init__(expression, parent)
		# Translate the comparator to a string
		self.__comparator = self.comparator_to_str(Compiler.get_attr(expression, 'ops')[0])
		# Left side
		self.__left = self.from_ast(Compiler.get_attr(expression, 'left'))
		# Right side
		self.__right = self.from_ast(Compiler.get_attr(expression, 'comparators')[0])

	def _transpile(self) -> str:
		"""
		Transpiles the comparison to a string.
		"""
		return f"{self.__left.transpile()}{self.__comparator}{self.__right.transpile()}"

	@staticmethod
	def comparator_to_str(comparator: cmpop) -> str:
		"""
		Transpiles an comparator to a string.

		:param comparator: The comparator to translate
		:return: The comparator as a C++ string.
		"""
		# Local import to avoid circular import errors
		from src.compiler.Constants import AST_COMPARATOR_TO_STR

		# Get the type
		comp_type = type(comparator)

		# Check if the operator is supported
		if comp_type in AST_COMPARATOR_TO_STR:
			# Return the translated operator
			return AST_COMPARATOR_TO_STR[comp_type]
		# Otherwise
		else:
			raise UnsupportedFeatureException(comparator)
