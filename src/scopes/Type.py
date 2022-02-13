"""
Variable class for scope handler.
"""
from collections import Callable
from dataclasses import dataclass
from typing import Any

from src.scopes.Object import Object
from src.structures.Errors import UnsupportedFeatureException


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

	def __init__(self, name: str) -> None:
		super().__init__(name)
		# Get the conversion function
		# Run it against the type name
		self.name = self.type_name_to_conversion_func(self.name)(self.name)

	def __hash__(self) -> int:
		"""
		Equality between objects is based on name.
		This has absolutely nothing to do with pass-by-value/pass-by-reference.
		What this means is that if somehow 2 instances of this class (Object
		or classes which inherit Object) are created for the same Python object,
		then when we == them, they will still show that they are the same object.
		"""
		return hash(self.name)

	@staticmethod
	def type_name_to_conversion_func(type_name: str) -> Callable[[Any], str]:
		"""
		Leverages the constant map to take a native type
		name and turn it into it's conversion function.
		The conversion function takes

		:param type_name: The name of the type to look up.
		:return: Returns the appropriate conversion function.
		"""
		from src.compiler.Constants import PY_CONSTANT_CONVERSION_FUNC

		# If we can convert it
		if type_name in PY_CONSTANT_CONVERSION_FUNC:
			# Then use the conversion table
			return PY_CONSTANT_CONVERSION_FUNC[type_name]
		else:
			# We can't use that
			raise UnsupportedFeatureException(type_name)
