"""
Class class for scope handler.
"""
from dataclasses import dataclass

from src.scopes.abstract.Object import Object
from src.scopes.abstract.Type import Type


@dataclass
class Class(Object):
	"""
	Class class, which inherits from the Object class.

	Holds relevant metadata about how this class operates.
	"""

	type: Type

