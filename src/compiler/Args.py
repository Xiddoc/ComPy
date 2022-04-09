"""
Singleton for the command line arguments.
"""
from argparse import Namespace
from dataclasses import dataclass, field
from typing import Optional

from src.structures.Errors import InvalidArgumentError
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
        # If the arguments were initialized (first usage of this class
        # was initialized with the arguments passed as a parameter to
        # the constructor).
        if self.__args is not None:
            # Then return it
            return self.__args

        # Otherwise, throw an error.
        # You must pass the command line arguments
        # for the first initialization of this
        # class (singleton class).
        raise InvalidArgumentError()
