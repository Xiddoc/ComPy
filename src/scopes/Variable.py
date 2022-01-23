"""
Variable class for scope handler.
"""
from dataclasses import dataclass
from typing import Any

from src.scopes.Object import Object


@dataclass
class Variable(Object):
	"""
	Variable class, which inherits from the Object class.

	Variables are objects which have a type, value, and name:

	- The name is inherited from the Object class.
	- The type must be set **ONCE** and can not be changed (freeing variables is not supported).
	- The value is only relevant to runtime. Since this is a *static* compiler, we only perform static type checking.
	"""

	type: str

	def __eq__(self, other: Any) -> bool:
		"""
		Equality between variables is based on name.
		This has absolutely nothing to do with pass-by-value/pass-by-reference.
		What this means is that if somehow 2 instances of this class (Variable)
		are created for the same Python variable, then when we == them, they
		will still show that they are the same variable.

		:param other: Another variable to check equality against.
		"""
		# Type check
		if not isinstance(other, Variable):
			raise TypeError()
		# Otherwise, compare the names
		return self.type == other.type
