"""
All new types which are just renames of other types.

This is for simplicitiy and conciseness, as sometimes
you will repeat a Union phrase often and will want to
cut down on the times you need to copy the type hint.
"""

from typing import Callable, Any, Union, Type, TYPE_CHECKING

# Prevent cyclic (recursive) imports
if TYPE_CHECKING:
	# noinspection PyUnresolvedReferences
	from src.pyexpressions.abstract.PyExpression import PyExpression

# A function with any parameters, which returns any value
AnyFunction = Callable[..., Any]

# A PyExpression or a class that extends it
GENERIC_PYEXPR_TYPE = Union["PyExpression"]
