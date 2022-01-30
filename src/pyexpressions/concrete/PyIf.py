"""
Class for a conditional statement.
"""
from _ast import If
from typing import Optional

from src.compiler.Compiler import Compiler
from src.pyexpressions.abstract.PyConditional import PyConditional
from src.pyexpressions.abstract.PyExpression import PyExpression
from src.structures.TypeRenames import GENERIC_PYEXPR_TYPE


class PyIf(PyConditional):
	"""
	Class for a Python conditional statement.
	"""

	__elif: Optional["PyIf"]
	__else: Optional[PyExpression]

	def __init__(self, expression: If, parent: GENERIC_PYEXPR_TYPE):
		super().__init__(expression, "if", parent)
		# If there is an "or else"
		orelse = Compiler.get_attr(expression, "orelse")[0]
		# Check that this is an if statement
		if isinstance(orelse, If):
			# Send to "if else"
			self.__elif = PyIf(orelse, self)
			self.__else = None
		else:
			# Send to "else"
			self.__elif = None
			self.__else = self.from_ast(orelse)

	def _transpile(self) -> str:
		"""
		Transpile the conditional statement to a string.
		"""
		return super()._transpile() + self.__elif.transpile() if self.__elif is not None else self.__else.transpile()
