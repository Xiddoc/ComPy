"""
Binary operation.
"""
from _ast import BinOp
from _ast import operator

from src.TypeRenames import GENERIC_PYEXPR_TYPE
from src.Errors import UnsupportedFeatureException
from src.pyexpressions.PyExpression import PyExpression


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
		self.__op_type = self.op_to_str(expression.op)
		# Store sides
		self.__left = self.from_ast(expression.left)
		self.__right = self.from_ast(expression.right)

	def __transpile(self) -> str:
		"""
		Transpile the operation to a string.
		@return:
		"""
		return "(" + self.__left.transpile() + self.__op_type + self.__right.transpile() + ")"

	@staticmethod
	def op_to_str(op: operator) -> str:
		"""
		Transpiles an operator to a string.

		@param op: The operator to translate
		@return: The operator as a C++ string.
		"""
		# Local import to avoid circular import errors
		from src.Constants import AST_OP_TO_STR

		# Get the operator type
		op_type = type(op)

		# Check if the operator is supported
		if op_type in AST_OP_TO_STR:
			# Return the translated operator
			return AST_OP_TO_STR[op_type]
		# Otherwise
		else:
			raise UnsupportedFeatureException(op)
