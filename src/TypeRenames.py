"""
All new types which are just renames of other types.

This is for simplicitiy and conciseness, as sometimes
you will repeat a Union phrase often and will want to
cut down on the times you need to copy the type hint.
"""

from typing import Callable, Any, Union, Type

# A function with any parameters, which returns any value
AnyFunction = Callable[..., Any]

# A PyExpression, class that extends a PyExpression, or PyPort
# Used for referring to PyExpressions and their likes as a whole
GENERIC_PYEXPR_TYPE = Union[Type["PyExpression"], "PyExpression", "PyPort"]
