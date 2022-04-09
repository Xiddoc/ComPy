"""
Class class for scope handler.
"""
from dataclasses import dataclass

from src.scopes.Scope import Scope
from src.scopes.abstract.Object import Object


@dataclass
class Class(Object):
    """
    Class class, which inherits from the Object class.

    Holds relevant metadata about how this class operates.
    We don't need to hold any "type" since the class is it's own type.
    In the future, we might want to check inheritance, for example.
    """

    scope: Scope

    def __hash__(self) -> int:
        """
        Equality between objects is based on name.
        This has absolutely nothing to do with pass-by-value/pass-by-reference.
        What this means is that if somehow 2 instances of this class (Object
        or classes which inherit Object) are created for the same Python object,
        then when we == them, they will still show that they are the same object.
        """
        return hash(self.name)
