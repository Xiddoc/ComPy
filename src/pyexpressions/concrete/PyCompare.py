"""
Comparison expression (condition).
"""
from _ast import Compare, cmpop
from typing import List

from src.compiler.Util import Util
from src.pyexpressions.abstract.PyExpression import PyExpression
from src.structures.Errors import UnsupportedFeatureException
from src.structures.TypeRenames import GENERIC_PYEXPR_TYPE


class PyCompare(PyExpression):
	"""
	Comparison expression (condition).
	"""

	__left: PyExpression
	__right: List[PyExpression]
	__comparators: List[str]

	def __init__(self, expression: Compare, parent: GENERIC_PYEXPR_TYPE):
		super().__init__(expression, parent)
		# Translate the comparator to a string
		self.__comparators = [self.comparator_to_str(comp) for comp in expression.ops]
		# Left side
		self.__left = self.from_ast(expression.left)
		# Translate each expression
		self.__right = [self.from_ast(expr) for expr in expression.comparators]

	def _transpile(self) -> str:
		"""
		Transpiles the comparison to a string.
		"""
		# The variable naming is slightly odd due to how the AST module names it's fields, but nevertheless-
		# The comparison should look something like this (example below):
		# left  comparators[0]  right[0]    comparators[1]  right[1] ...
		# 5     <               6           <               7

		return self.__left.transpile() + \
			''.join([item[0] + item[1].transpile() for item in zip(self.__comparators, self.__right)])

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
