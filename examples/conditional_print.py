"""
Print a string forever, recursively.
"""


def conditional_print(index: int) -> None:
    """
    Print a string, depending on the condition met.
    Should print:

    [my_string]1
    [my_string]2
    [my_string]3
    ...

    :param index: The current looping index.
    """

    # Equal to 0, and not equal to 2, and not equal to 3
    if index == 0 and index != 2 and index != 3:
        print(str(index) + ": Equals to 0!")
    # If 1 is smaller than 2, and 2 is smaller than index, and index is smaller than 5
    elif 1 < 2 < index < 5:
        print(str(index) + ": Larger than 2 and smaller than 5!")
    # If index is larger than 7 and smaller than 12
    elif 7 < index < 12:
        print(str(index) + ": Larger than 7 and smaller than 12!")
    else:
        # Otherwise,
        print(str(index) + ": Other...")
        # If index is 4 (should never run, since it will be caught between the "1 < 2 < index < 5" statement
        if index == 4:
            print(str(index) + ": Test, got 4...")

    # Recursion!
    conditional_print(index + 1)


# Should cause a StackOverflow
# due to excessive recursion...
conditional_print(0)
