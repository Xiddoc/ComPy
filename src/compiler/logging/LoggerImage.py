"""
Class to help structure the AST in order for it to be rendered.
"""
from typing import Dict, Union

from ete3 import TreeStyle, Tree, TextFace

from src.compiler.Args import Args
from src.compiler.Util import Util
from src.pyexpressions.abstract.PyExpression import PyExpression
from src.structures.Singleton import Singleton


class LoggerImage(metaclass=Singleton):
    """
    A class to structure the AST into the Newick
    format (also known as a Newick tree), which can
    then be rendered into an image.
    """

    __node_parents: Dict[int, Union[int, None]]
    __node_hashes: Dict[int, PyExpression]
    __const_style: TreeStyle

    def __init__(self) -> None:
        # Each element should list their hash and their parent's expression here
        self.__node_parents = {}
        # Each element should list their hash and their expression here
        self.__node_hashes = {}
        # Define the style of the tree, for when we render it
        self.__const_style = TreeStyle()
        self.__const_style.show_leaf_name = False
        self.__const_style.show_branch_length = False
        self.__const_style.show_border = True
        self.__const_style.show_scale = False
        self.__const_style.margin_top = 75
        self.__const_style.margin_right = 75
        self.__const_style.margin_bottom = 75
        self.__const_style.margin_left = 75
        self.__const_style.scale = 50
        self.__const_style.min_leaf_separation = 50

    def add_node(self, node: PyExpression) -> None:
        """
        Adds the PyExpression node to the Newick tree.

        :param node: The expression node to insert.
        """
        # Get the parent node
        parent = node.get_parent()
        # Add the node to our dictionary so we can turn it into a tree later
        self.__node_parents[id(node)] = None if parent is None else id(parent)
        self.__node_hashes[id(node)] = node

    def render(self) -> None:
        """
        Compiles the AST tree to a Newick formatted tree,
        then renders it all to an image and saves it to a file.
        """
        # Get the top-most node
        top_node: int = -1
        # Make a dictionary to hold the organized tree
        inversed_dict = {}
        # For each node and its parent
        for node_id, parent_id in self.__node_parents.items():
            # Get the top-most node (will have no parent, or in other words their parent is None)
            if parent_id is None:
                top_node = node_id
                # Don't add it to the rest of the dictionary
                continue
            # If the parent already exists, then create an array with the node
            # Otherwise, add the child node to the list of children nodes ([] + [] is an append)
            inversed_dict[parent_id] = inversed_dict.get(parent_id, []) + [node_id]

        # Define a function for us to use recursion
        def format_node(current_node: int) -> str:
            """
            Recursively represents a node and all its children as a Newick tree.

            :return: A Newick formatted string.
            """
            from src.compiler.logging.Logger import Logger

            # We will build the description that will be used as the "leaf text" in the image tree
            # Get the expression name
            expr_name = Util.get_name(self.__node_hashes[current_node])
            # Get a short debugging description
            # Escape all quotation marks (") since we will be putting this
            # debug text inside another set of wrapping quotation marks
            short_desc = Logger.short_describe_node(self.__node_hashes[current_node]).replace('"', '\\"')
            # Generate the tree leaf's text
            if short_desc:
                leaf_text = f'"{expr_name}: {short_desc}"'
            else:
                leaf_text = f'"{expr_name}"'

            # Recursion condition: If we have children, then recurse, otherwise return our formatted string
            # Get this node's children
            children = inversed_dict.get(current_node)
            # If this node has children
            if children:
                # Recursively operate for children
                formatted_children = ",".join([format_node(child) for child in children])
                # Build it using the parenthesis format
                return f'({formatted_children}){leaf_text}'
            else:
                # Otherwise, just add a short description
                return leaf_text

        # Call the recursive function to format the node
        newick_tree: str = f"{format_node(top_node)};"

        # Create a visual tree using the our formatted tree
        t = Tree(newick_tree, format=8, quoted_node_names=True)

        # There is no other way to show internal nodes, or
        # basically every node that is not a final/leaf node
        for node in t.traverse():
            node.add_face(TextFace(text=node.name, fsize=13, tight_text=True), column=0)

        # Render the tree to an image
        from src.compiler.logging.Logger import Logger
        Logger.log(f"Rendering debugging image...")
        output_file = Args().get_args().file.name + ".png"
        t.render(file_name=output_file, tree_style=self.__const_style)
        Logger.log(f"Wrote image to output file '{output_file}'...")
