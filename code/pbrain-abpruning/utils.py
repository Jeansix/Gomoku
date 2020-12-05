def get_all_around(pos):
    """Get all positions around the given pos.

    Args:
        pos:current position

    Returns:
        list of around positions

    """
    x, y = pos
    return [(nx, ny) for nx in [x - 1, x, x + 1] for ny in [y - 1, y, y + 1]]


