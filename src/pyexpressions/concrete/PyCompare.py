"""
Comparison expression (condition).
"""
from _ast import Compare, cmpop
from typing import List

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

		# So in order to iterate over this, and split up into comparisons like the following:
		# 5 < 6 and 6 < 7 and ...

		# Then we need to iterate like so:
		# LEFT      COMPARATORS[0]  RIGHT[0]
		# RIGHT[0]  COMPARATORS[1]  RIGHT[1]
		# RIGHT[1]  COMPARATORS[2]  RIGHT[2]
		# RIGHT[2]  COMPARATORS[3]  RIGHT[3]
		# ...       ...             ...

		# We will do this using the zip() function, and by making a new list where the LEFT expression is first
		# Make the new list
		left_list: List[PyExpression] = [self.__left] + self.__right
		# Zip them together (iterate, where each iteration yields a LEFT, a COMPARATOR, and a RIGHT)
		# Then, join all the comparisons together with the 'AND' boolean operation
		return ' && '.join([
			f"{L.transpile()} {C} {R.transpile()}" for L, C, R in zip(left_list, self.__comparators, self.__right)
		])

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
