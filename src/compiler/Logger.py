"""
Logging utilities and functions.
"""
from threading import Thread, Event
from tkinter import Tk, END, PhotoImage
from tkinter.ttk import Treeview, Style
from typing import cast, List

from src.compiler.Args import Args
from src.compiler.Util import Util
from src.pyexpressions.abstract.PyExpression import PyExpression
from src.pyexpressions.concrete.PyConstant import PyConstant
from src.pyexpressions.concrete.PyExpr import PyExpr
from src.pyexpressions.highlevel.PyIdentifiable import PyIdentifiable
from src.structures.Singleton import Singleton


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
    def is_debug() -> bool:
        """
        :return: True if any debugging flags are turned on.
        """
        return \
            Args().get_args().debug_gui or \
            Args().get_args().debug_text or \
            Args().get_args().debug_image

    @staticmethod
    def update_debug_viewer() -> None:
        """
        Wrapper method to update the AST debug GUI.
        """
        # Check if logging is enabled
        if Args().get_args().debug_gui:
            # Update the tree
            LoggerGUI().update_tree()

    def log_tree_up(self, message: str) -> None:
        """
        Logs a string to standard output.
        Automatically formats the string with a tree
        that points upwards (branches head down).

        :param message: The message to log.
        """
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

        :param message: The message to log.
        """
        # Check if logging is enabled
        if Args().get_args().debug_text:
            # If it is, then print the message
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


class LoggerGUI(metaclass=Singleton):
    """
    A Tkinter Graphical User Interface used for displaying
    the ComPy Abstract Syntax Tree in an interactive form.
    """

    __window: Tk
    __tree: Treeview
    __window_ready: Event
    __listed_nodes: List[PyExpression]

    def __init__(self) -> None:
        # Create an event to block the core thread while the GUI is not yet ready
        self.__window_ready = Event()
        # Create the window and basic elements in a new thread
        # This is so that the GUI event loop does not block the compiler
        self.__listed_nodes = []
        Thread(target=self.create_window).start()

    def create_window(self) -> None:
        """
        Creates the Tkinter window and elements necessary
        for displaying the Abstract Syntax tree.
        """
        # Create a root window
        self.__window = Tk()
        self.__window.title('ComPy AST Viewer')
        self.__window.geometry('700x500')
        # noinspection PyArgumentEqualDefault
        self.__window.wm_iconphoto(False, PhotoImage(file="resources/compy.png"))
        # Tkinter uses a grid-based layout
        self.__window.rowconfigure(0, weight=1)
        self.__window.columnconfigure(0, weight=1)
        # Create style for fonts and overall window theme
        custom_style = Style()
        custom_style.theme_use("clam")  # Themes: 'winnative', 'clam', 'alt', 'default', 'classic', 'vista', 'xpnative'
        custom_style.configure("Treeview", font=('Lucida Console', 11))
        # Create a tree view to display the AST (second parameter removes the header line)
        self.__tree = Treeview(self.__window, show="tree")
        # Place the element inside the root window's grid, and expand it to the max size
        # (NSEW = North, East, South, West)
        self.__tree.grid(row=0, column=0, sticky='NESW')
        # Release the thread lock
        self.__window_ready.set()
        # Show the window
        self.__window.mainloop()

    def add_node(self, node: PyExpression) -> None:
        """
        Adds the PyExpression node to the GUI.

        :param node: The expression node to insert.
        """
        # Wait until the GUI is ready
        # This function call is BLOCKING and will not return until the lock is released
        self.__window_ready.wait()
        # The parameter takes a blank string to set no parent (top level)
        # Otherwise, pass the memory ID of the parent expression
        parent: str = '' if node.get_parent() is None else str(id(node.get_parent()))
        # Insert the node into the tree, at the end of the parent list
        # Set the node's tree ID to its object's ID
        self.__tree.insert(
            parent=parent,
            index=END,
            iid=str(id(node)),
            text="Loading..."
        )
        # Add the node to our cache so we can update it later
        self.__listed_nodes.append(node)

    def update_tree(self) -> None:
        """
        Updates all the nodes in the tree element with their proper debug information.

        This is called here, as opposed to during the creation of the tree element,
        since only now are all the PyExpressions fully initialized. If this were
        executed during the tree creation, it is possible that attempting to fetch
        some of the debug information will not work, since the expression has not
        yet parsed the data necessary from its parents.
        """
        # Update each element in the tree
        for node in self.__listed_nodes:
            # Add some informational text for each tree node
            extra_text = "Expand for more information"
            # Look up object from its memory ID
            if isinstance(node, PyExpr) or isinstance(node, PyConstant):
                # Get the transpiled constant
                extra_text = node.transpile()
            elif isinstance(node, PyIdentifiable):
                # Get the virtual ID of the expression
                extra_text = node.get_id()
            # Update the debug info in the GUI element
            self.__tree.item(str(id(node)), text=f"{Util.get_name(node)}: {extra_text}")
