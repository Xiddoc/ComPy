"""
Error classes, when needed for exceptions.
"""
from _ast import AST

from dataclasses import dataclass, field
from typing import Optional


@dataclass(frozen=True)
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


@dataclass(frozen=True)
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


@dataclass(frozen=True)
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


@dataclass(frozen=True)
class InvalidArgumentError(ValueError):
	"""
	An error to throw when the user inputted an invalid argument.
	Specifically, to be used for command line arguments. Not for
	syntax arguments / code that is currently being compiled.
	"""

	argument: Optional[str] = field(default=None)

	def __str__(self) -> str:
		# Error text
		return \
			f"Argument '{self.argument}' is not valid." \
			if self.argument is not None else \
			"Internal argument handling error encountered."


@dataclass(frozen=True)
class InvalidTypeError(TypeError):
	"""
	An error to throw when the user gave an invalid type or
	value of a non-corresponding type (in their syntax/code).
	"""

	given_type: Optional[str] = field(default=None)
	expected_type: Optional[str] = field(default=None)

	def __str__(self) -> str:
		# Error text
		return \
			f"Could not use type '{self.given_type}' when type '{self.expected_type}' was expected." \
			if self.given_type is not None else \
			"Invalid types (or value of conflicting type) found in code."
