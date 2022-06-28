"""
Utility functions, methods, classes,
and other useful tools to help cut
and clean the code base.
"""
from _ast import AST
from functools import reduce
from math import floor, log
from typing import Any, Union
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.pyexpressions.abstract.PyExpression import PyExpression


class Util:
    """
    Static utility class.
    """

    @staticmethod
    def get_attr(obj: Union[AST, "PyExpression"], attribute_path: str) -> Any:
        """
        A function that recursively traverses down an "attribute path"
        and retrieves the value at the end of the path.

        This function exists since the CPython ast library uses an odd
        system which dynamically adds attributes to the AST instances,
        instead of statically declaring them in their respective classes.

        Due to this, mypy will throw a type-checking error since it will
        not find these attributes in the class definition. Hence, to work
        around this bug, we will use the getattr function to retrieve the
        attributes directly.

        :param obj: The AST object to traverse.
        :param attribute_path: The attribute path to use (for example, if passing
                                the object 'expression', and you want to navigate
                                to the 'target' attribute, then the 'id' attribute
                                of the 'target' attribute, then for this parameter
                                you would pass the string "target.id").
        """
        # Split by .
        # For example: "expression.target.id" becomes ["expression", "target", "id"]
        attrs = attribute_path.split(".")

        # Cumulatively execute the "getattr" function
        # On the first 2 arguments of the list
        return reduce(getattr, attrs, obj)

    @classmethod
    def get_name(cls, obj: Union[AST, "PyExpression"]) -> str:
        """
        Retrieves the name of the AST node's class.
        For example, instead of seeing: <ast.AnnAssign object at 0x000002CC7FE5A310>
        You could use this method to abbreviate to: AnnAssign

        :param obj: An instance of the AST expression or node to name.
        :return: The string representation of the AST node's class name.
        """
        return str(cls.get_attr(obj, "__class__.__name__"))

    @staticmethod
    def escape(string: str) -> str:
        """
        Escapes a Python string of newlines
        and other formats in order to form
        a consistent one-line string.

        :param string: The string to escape.
        :return: The escaped one-line string.
        """
        # Import locally to avoid cyclic import error
        from src.compiler.Constants import PY_SPECIAL_CHARS

        # For each special character
        for special_char, escaped_char in PY_SPECIAL_CHARS.items():
            # Replace with the escaped version
            string = string.replace(special_char, escaped_char)

        # Return escaped version
        return string

    @staticmethod
    def represent_file_size(file_size: int) -> str:
        """
        Convert a file size to a string representation.
        For example, if you pass the integer 2048, then you will get "2.0 KB" returned.

        :param file_size: The file size (in bytes) to convert to a string.
        :return: A string representing the file size with an abbreviation.
        """
        # Critical case
        if file_size == 0:
            return "0 B"

        # All the different possible representations
        size_names = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
        # How many orders of 1024 is the file size?
        # (from each index, such as B to KB, the magnitude increases by 1024)
        size_name_index = int(floor(log(file_size, 1024)))
        # Convert the file size to the selected magnitude
        # Get the size name by index
        # Format into a string, then return the string
        return f"{round(file_size / pow(1024, size_name_index), 2)} {size_names[size_name_index]}"
