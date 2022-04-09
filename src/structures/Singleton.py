"""
Python Singleton implementation.
"""
from typing import Dict, Any


class Singleton(type):
    """
    Singleton implementation.

    Use this as a metaclass for other classes
    which you want to be singletons.
    """

    # The key is the class type. For example, class A.
    # The value is an instance of the class. For example, <A at 0x1df975376d0>
    __instances: Dict["Singleton", "Singleton"] = {}

    def __call__(cls, *args: Any, **kwargs: Any) -> "Singleton":
        # Check if there is already an instance registered
        if cls not in cls.__instances:
            # If there are no instances for this type of class
            # Then instantiate a new instance for this class
            # Add it to the dictionary
            cls.__instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)

        # Return the instance of the class
        return cls.__instances[cls]
