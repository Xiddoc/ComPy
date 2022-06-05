"""
Class to build the Logging GUI.
"""
from threading import Event, Thread
from tkinter import Tk, PhotoImage, END
from tkinter.ttk import Treeview, Style
from typing import List

from src.compiler.Util import Util
from src.pyexpressions.abstract.PyExpression import PyExpression
from src.structures.Singleton import Singleton


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
        from src.compiler.logging.Logger import Logger
        # Update each element in the tree
        for node in self.__listed_nodes:
            # Get a short description
            short_desc = Logger.short_describe_node(node)
            # Format the node into a nice debug string
            # If there is no description, write a little "expand" message
            debug_text = f"{Util.get_name(node)}: {short_desc if short_desc else 'Expand for more information'}"
            # Update the debug info in the GUI element
            self.__tree.item(str(id(node)), text=debug_text)
