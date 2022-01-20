"""
Error classes, when needed for exceptions.
"""
from _ast import AST


class VariableAlreadyDefinedError(NameError):
	"""
	For our compilation scheme, variables can only be defined once and must be given a type hint.
	If you try to type hint the same variable 2 times, this should raise an error.
	From this, you should also realize that variable types are immutable and cannot be freed.
	"""


class VariableNotDefinedError(NameError):
	"""
	As stated in VariableAlreadyDefinedError, a variable must have an explicit type hint the first time it is used.
	This is referred to as "defining" or "initializing".
	If a variable is referenced without being defined, then the compiler should throw this error.
	"""


class UnsupportedFeatureException(SyntaxError):
	"""
	An error to raise whenever a Python feature is used which is not implemented in the compiler.
	Examples (currently) include classes, for example. (Boo hoo, no OOP for you)
	"""

	feature: AST

	def __init__(self, feature: AST) -> None:
		self.feature = feature

	def __str__(self) -> str:
		# Local import to avoid import error
		from src.Compiler import Compiler
		# Error text
		return f"Python feature '{Compiler.get_attr(self.feature, '__class__.__name__')}' is not supported by the compiler."
