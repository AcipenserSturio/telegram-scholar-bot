import itertools

def first(iterable):
    # Try to get the first item from iterable. Suppress errors.
    try:
        first = next(iterable)
    except StopIteration:
        return None
    return first
