"""
Logging utilities and functions.
"""
from typing import cast

from src.compiler.Args import Args
from src.compiler.logging.LoggerGUI import LoggerGUI
from src.compiler.logging.LoggerImage import LoggerImage
from src.pyexpressions.abstract.PyExpression import PyExpression
from src.pyexpressions.concrete.PyConstant import PyConstant
from src.pyexpressions.concrete.PyExpr import PyExpr
from src.pyexpressions.highlevel.PyIdentifiable import PyIdentifiable


class Logger:
    """
    Logger class.

    Lightweight instance that belongs to and
    is passed between to each classes.
    """

    __indentation: int = 0

    def __init__(self, py_expr: PyExpression) -> None:
        # Check if logging is enabled
        if not self.is_debug():
            # If not then no need to calculate expensive recursive logging operations
            return

        # Add this expression to the AST GUI
        if Args().get_args().debug_gui:
            LoggerGUI().add_node(py_expr)

        # Add this expression to the AST image
        if Args().get_args().debug_image:
            LoggerImage().add_node(py_expr)

        # Figure out indentation level
        # We do this by figuring out how many parents there are to this node.
        temp_expr: PyExpression = py_expr
        indentation: int = 0

        # Keep iterating up the "parent node chain" until
        # we hit the edge of the Module scope (outer layer)
        while not temp_expr.is_exterior_scope():
            # Increment the count
            indentation += 1
            # Iterate to next parent
            # Cast to PyExpression since the while loop condition has validated that
            temp_expr = cast(PyExpression, temp_expr.get_parent())

        # Set to field
        self.__indentation = indentation

    @staticmethod
    def short_describe_node(node: PyExpression) -> str:
        """
        Take a PyExpression node and convert it to a small description.

        :return: A small description of the node, as a string.
                If no description can be produced, returns an empty string.
        """
        # Add some informational text for each tree node
        desc = ""
        # Look up object from its memory ID
        if isinstance(node, PyExpr) or isinstance(node, PyConstant):
            # Get the transpiled constant
            desc = node.transpile()
        elif isinstance(node, PyIdentifiable):
            # Get the virtual ID of the expression
            desc = node.get_id()
        # Return the description
        return desc

    @staticmethod
    def is_debug() -> bool:
        """
        :return: True if any debugging flags are turned on.
        """
        return \
            Args().get_args().debug_gui or \
            Args().get_args().debug_text or \
            Args().get_args().debug_image

    @staticmethod
    def finalize_debuggers() -> None:
        """
        Wrapper method to update the AST debuggers.
        """
        # Check if GUI logging is enabled
        if Args().get_args().debug_gui:
            # Update the tree
            LoggerGUI().update_tree()

        if Args().get_args().debug_image:
            # Render the image
            LoggerImage().render()

    def log_tree_up(self, message: str) -> None:
        """
        Logs a string to standard output.
        Automatically formats the string with a tree
        that points upwards (branches head down).

        :param message: The message to log.
        """
        # Check if logging is enabled
        if Args().get_args().debug_text:
            # Merge the tree branches with the message
            # Log it
            self.log(
                self.__get_log_prepend(
                    indentation=self.__indentation,
                    point_upwards=True
                ) + message
            )

    def log_tree_down(self, message: str) -> None:
        """
        Logs a string to standard output.
        Automatically formats the string with a tree
        that points downwards (branches head up).

        :param message: The message to log.
        """
        # Check if logging is enabled
        if Args().get_args().debug_text:
            # Merge the tree branches with the message
            # Log it
            self.log(
                self.__get_log_prepend(
                    indentation=self.__indentation,
                    point_upwards=False
                ) + message
            )

    @staticmethod
    def log(message: str) -> None:
        """
        Logs a string to standard output.
        While this seems unnecessary, this is good practice for developing
        wrapper functions. Later, if I want, I only have to change this function
        if I want to alter the console logging across the entire project.
        For example, if I wanted to add colors to the console output, I could add it here.

        :param message: The message to log.
        """
        # Print the input message
        print(message)

    @staticmethod
    def __get_log_prepend(indentation: int, point_upwards: bool) -> str:
        """
        Creates the tree indentation string.

        :param indentation: The amount to indent into the tree.
        :return: A string of unicode symbols, spaces, and newlines which forms one line of the tree.
        """
        # If first layer of tree, then use T symbol
        if indentation == 1:
            return "├── "
        # If the indentation is any more than 1, then place root branch on first line
        # Then, branch off of the previous node (hence, indentation - 1)
        elif indentation > 1:
            return "│" + "\t" * (indentation - 1) + ("└" if point_upwards else "┌") + "── "
        # Otherwise, if this is the root branch (layer zero)
        # Make a newline to separate from previous node tree.
        return "\n"
