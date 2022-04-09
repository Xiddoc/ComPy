"""
Testing a class in Python.
"""


class TestClass:
    """
    Class documentation.
    """

    test_field: int

    def __init__(self) -> None:
        # Initialize new temporary variable
        test_var: int = 1
        # Print it
        print(test_var)


# Initialize the class
test_instance: TestClass = TestClass()

# Get a public field
print(test_instance.test_field)
