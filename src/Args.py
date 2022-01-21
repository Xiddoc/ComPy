"""
Singleton for the command line arguments.
"""
from argparse import Namespace
from dataclasses import dataclass, field
from typing import Optional

from src.structures.Singleton import Singleton


# Freeze the class, meaning that the fields will be read-only
@dataclass(frozen=True)
class Args(metaclass=Singleton):
	"""
	Command line argumnets, parsed.
	"""

	# As this is a singleton, these arguments will
	# only be assigned once, by the main script.
	__args: Optional[Namespace] = field(default=None)

	def get_args(self) -> Namespace:
		"""
		Getter function for arguments.
		"""
		return self.__args
