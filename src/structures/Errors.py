"""
Error classes, when needed for exceptions.
"""
from _ast import AST
from dataclasses import dataclass, field
from typing import Optional, Union

from src.compiler.Util import Util


@dataclass(frozen=True)
class ObjectAlreadyDefinedError(NameError):
	"""
	For our compilation scheme, objects can only be defined once and must be given a type hint.
	If you try to type hint the same object 2 times, this should raise an error.
	From this, you should also realize that object types are immutable and cannot be freed.
	"""

	object_name: str

	def __str__(self) -> str:
		# Error text
		return f"You cannot redefine object '{self.object_name}' as it is already initialized."


@dataclass(frozen=True)
class ObjectNotDefinedError(NameError):
	"""
	As stated in ObjectAlreadyDefinedError, a object must have an explicit type hint the first time it is used.
	This is referred to as "defining" or "initializing".
	If a object is referenced without being defined, then the compiler should throw this error.
	"""

	object_name: str

	def __str__(self) -> str:
		# Error text
		return f"Object '{self.object_name}' was not initialized yet."


@dataclass(frozen=True)
class UnsupportedFeatureException(SyntaxError):
	"""
	An error to raise whenever a Python feature is used which is not implemented in the compiler.
	Examples (currently) include classes, for example. (Boo hoo, no OOP for you)
	"""

	feature: Union[AST, str]

	def __str__(self) -> str:
		# Local import to avoid import error
		# Error text
		return "Python feature '" + \
				(Util.get_name(self.feature) if isinstance(self.feature, AST) else self.feature) + \
				"' is not supported by the compiler."


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
		return f"Argument '{self.argument}' is not valid." \
				if self.argument is not None else \
				"Internal argument handling error encountered."


@dataclass(frozen=True)
class SyntaxSubsetError(SyntaxError):
	"""
	An error to throw when the user's code does
	not match the syntax subset specifications.
	"""

	warning: str = field()

	def __str__(self) -> str:
		# Error text
		return f"Invalid usage of '{self.warning}' caused a syntax error (the code must comply to the syntax subset)."


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
		return f"Could not use type '{self.given_type}' when type '{self.expected_type}' was expected." \
				if self.given_type is not None else \
				"Invalid types (or value of conflicting type) found in code."
