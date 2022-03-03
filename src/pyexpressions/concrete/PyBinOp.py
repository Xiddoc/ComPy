"""
Binary operation.
"""
from _ast import BinOp
from _ast import operator

from src.pyexpressions.abstract.PyExpression import PyExpression
from src.structures.Errors import UnsupportedFeatureException
from src.structures.TypeRenames import GENERIC_PYEXPR_TYPE


class PyBinOp(PyExpression):
	"""
	Expression for binary operation.
	"""

	__left: PyExpression
	__right: PyExpression
	__op_type: str

	def __init__(self, expression: BinOp, parent: GENERIC_PYEXPR_TYPE):
		super().__init__(expression, parent)
		# Convert op to string
		self.__op_type = self.bin_op_to_str(expression.op)
		# Store sides
		self.__left = self.from_ast(expression.left)
		self.__right = self.from_ast(expression.right)

	def _transpile(self) -> str:
		"""
		Transpile the operation to a string.
		"""
		return f"({self.__left.transpile()} {self.__op_type} {self.__right.transpile()})"

	@staticmethod
	def bin_op_to_str(op: operator) -> str:
		"""
		Transpiles a binary operator to a string.

		:param op: The operator to translate
		:return: The operator as a C++ string.
		"""
		# Local import to avoid circular import errors
		from src.compiler.Constants import AST_OP_TO_STR

		# Get the operator type
		op_type = type(op)

		# Check if the operator is supported
		if op_type in AST_OP_TO_STR:
			# Return the translated operator
			return AST_OP_TO_STR[op_type]
		# Otherwise
		else:
			raise UnsupportedFeatureException(op)
