"""
Assign via augmented assignment to a variable.
"""
from _ast import AugAssign

from src.compiler.Util import Util
from src.pyexpressions.abstract.PyExpression import PyExpression
from src.pyexpressions.concrete.PyBinOp import PyBinOp
from src.structures.TypeRenames import GENERIC_PYEXPR_TYPE


class PyAugAssign(PyExpression):
	"""
	Expression for assigning a variable via augmented assignment.
	"""

	__target: str
	__op_type: str
	__value: PyExpression

	def __init__(self, expression: AugAssign, parent: GENERIC_PYEXPR_TYPE):
		super().__init__(expression, parent)

		# Store variable and operation
		self.__target = Util.get_attr(expression, "target.id")
		self.__op_type = PyBinOp.bin_op_to_str(Util.get_attr(expression, "op"))
		# Convert and store the value that is being operated with
		self.__value = self.from_ast(Util.get_attr(expression, "value"))

	def _transpile(self) -> str:
		"""
		Transpile the operation to a string.
		"""
		return f"{self.__target} {self.__op_type}= {self.__value.transpile()}"
