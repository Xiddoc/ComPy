"""
Object class for scope handler.
"""

from dataclasses import dataclass


@dataclass
class Object:
    """
    Specifies basic attributes which all objects should have.

    An example of this would be a name- all objects have names:
    functions, variables, classes, etc. (Although you could argue
    lambda expressions don't fit this category, we can specify
    an exception for them, such as setting the name to blank or
    None).
    """

    name: str
