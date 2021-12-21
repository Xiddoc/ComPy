"""
Binary operation.
"""
from _ast import BinOp
from _ast import operator, Add, Sub, Mult
from typing import Dict, Type

from Errors import UnsupportedFeatureException
from expressions.PyExpression import PyExpression


class PyBinOp(PyExpression):
	"""
	Expression for binary operation.
	"""

	__left: PyExpression
	__right: PyExpression
	__op_type: str

	def __init__(self, expression: BinOp):
		super().__init__(expression)
		# Convert op to string
		self.__op_type = self.op_to_str(expression.op)
		# Store sides
		self.__left = PyExpression.from_expr(expression.left)
		self.__right = PyExpression.from_expr(expression.right)

	def transpile(self) -> str:
		"""
		Transpile the operation to a string.
		@return:
		"""
		return self.__left.transpile() + self.__op_type + self.__right.transpile()

	@staticmethod
	def op_to_str(op: operator) -> str:
		"""
		Transpiles an operator to a string.

		@param op: The operator to translate
		@return: The operator as a C++ string.
		"""
		# Get the operator type
		op_type = type(op)
		# Check if the operator is supported
		if op_type in AST_OP_TO_STR:
			# Return the translated operator
			return AST_OP_TO_STR[op_type]
		# Otherwise
		else:
			raise UnsupportedFeatureException(
				f"Python feature '{op.__name__}' is not supported by the compiler.")


AST_OP_TO_STR: Dict[Type[operator], str] = {
	Add: "+",
	Sub: "-",
	Mult: "*"
}
