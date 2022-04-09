"""
Variable class for scope handler.
"""
from dataclasses import dataclass

from src.scopes.abstract.Object import Object


@dataclass
class Type(Object):
	"""
	Type class, which inherits from the Object class.

	Types are objects which have a name, and
	are sometimes converted to native counterparts.

	For example, when type hinting 'Any' in Python, the
	pseudo-equivalent would be the 'auto' keyword. I am
	aware that there are problems that could arise from
	this, such as simple invalid types, but the compiler
	is still in beta mode and this is the best we can do
	for now.
	"""

	def __hash__(self) -> int:
		"""
		Equality between objects is based on name.
		This has absolutely nothing to do with pass-by-value/pass-by-reference.
		What this means is that if somehow 2 instances of this class (Object
		or classes which inherit Object) are created for the same Python object,
		then when we == them, they will still show that they are the same object.
		"""
		return hash(self.name)
