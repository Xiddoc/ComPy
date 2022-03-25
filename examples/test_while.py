"""
Let's try to use a while loop.
"""

index: int = 0

# Loop 100 times
while index < 100:
    # Print our index
    print("Index is: " + str(index))
    # Increment our index
    index += 1

    if index == 88:
        # Test breaking the loop
        break
