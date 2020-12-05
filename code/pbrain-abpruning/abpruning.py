class Node:
    def __init__(self):

    




def maxValue(node, alpha, beta):
    """Get value for the given MAX node.

    Args:
        node: class Node object
        alpha: float
        beta: float

    Returns:
        value of the node

    """
    if node.is_leaf:
        return node.value
    val = float("-inf")
    for successor in node.successor:
        val = max(val, minValue(successor, alpha, beta))
        if val >= beta:
            return val
        alpha = max(alpha, val)
    return val


def minValue(node, alpha, beta):
    """Get value for the given MIN node.

    Args:
        node: class Node object
        alpha: float
        beta: float

    Returns:
        value of the node

    """
    if node.is_leaf:
        return node.value
    val = float("inf")
    for successor in node.successor:
        val = min(val, maxValue(successor, alpha, beta))
        if val <= alpha:
            return val
        beta = min(beta, val)
    return val
