import itertools

def peek(iterable):
    # Check if iterable contains items,
    # but put the item back after checking
    try:
        first = next(iterable)
    except StopIteration:
        return None
    return first, itertools.chain([first], iterable)
