"""
Class for a conditional statement.
"""
from _ast import If
from typing import Optional, List

from src.compiler.Util import Util
from src.pyexpressions.abstract.PyConditional import PyConditional
from src.pyexpressions.abstract.PyExpression import PyExpression
from src.structures.TypeRenames import GENERIC_PYEXPR_TYPE


class PyIf(PyConditional):
	"""
	Class for a Python conditional statement.
	"""

	__elif: Optional["PyIf"]
	__else: Optional[List[PyExpression]]

	def __init__(self, expression: If, parent: GENERIC_PYEXPR_TYPE, if_type: str = "if"):
		super().__init__(expression, if_type, parent)
		# Defaults
		self.__elif = None
		self.__else = None
		# If there is an "or else"
		orelse_list = expression.orelse
		if orelse_list:
			# If this is a singular "If" expression,
			# then this is meant to be an "elif" statement
			if len(orelse_list) == 1 and isinstance(orelse_list[0], If):
				# Send to "if else"
				self.__elif = PyIf(orelse_list[0], self, if_type="else if")
			else:
				# Send to "else"
				self.__else = [self.from_ast(ast) for ast in orelse_list]

	def _transpile(self) -> str:
		"""
		Transpile the conditional statement to a string.
		"""
		return super()._transpile() + \
			self.__elif.transpile() if self.__elif is not None else \
			f"else {{{''.join([expr.transpile() for expr in self.__else])}}}" if self.__else is not None else \
			""
