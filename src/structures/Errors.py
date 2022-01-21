"""
Error classes, when needed for exceptions.
"""
from _ast import AST

from dataclasses import dataclass
from typing import Optional


@dataclass
class VariableAlreadyDefinedError(NameError):
	"""
	For our compilation scheme, variables can only be defined once and must be given a type hint.
	If you try to type hint the same variable 2 times, this should raise an error.
	From this, you should also realize that variable types are immutable and cannot be freed.
	"""

	variable_name: str

	def __str__(self) -> str:
		# Error text
		return f"You cannot redefine variable '{self.variable_name}' as it is already initialized."


@dataclass
class VariableNotDefinedError(NameError):
	"""
	As stated in VariableAlreadyDefinedError, a variable must have an explicit type hint the first time it is used.
	This is referred to as "defining" or "initializing".
	If a variable is referenced without being defined, then the compiler should throw this error.
	"""

	variable_name: str

	def __str__(self) -> str:
		# Error text
		return f"Variable '{self.variable_name}' was not initialized yet."


@dataclass
class UnsupportedFeatureException(SyntaxError):
	"""
	An error to raise whenever a Python feature is used which is not implemented in the compiler.
	Examples (currently) include classes, for example. (Boo hoo, no OOP for you)
	"""

	feature: AST

	def __str__(self) -> str:
		# Local import to avoid import error
		from src.Compiler import Compiler
		# Error text
		return f"Python feature '{Compiler.get_name(self.feature)}' is not supported by the compiler."


class InvalidArgumentError(ValueError):
	"""
	An error to throw when the user inputted an invalid argument.
	Specifically, to be used for command line arguments. Not for
	syntax arguments / code that is currently being compiled.
	"""

	argument: Optional[str]

	def __str__(self) -> str:
		# Error text
		return \
			f"Argument '{self.argument}' is not valid." \
			if self.argument is not None else \
			"Internal argument handling error encountered."