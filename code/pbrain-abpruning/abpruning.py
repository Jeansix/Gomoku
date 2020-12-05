import utils

board_size = 20


class Node:
    """Node of the tree.

    Attributes:
        state: tuple,(stones,playing)
               stones: list of sets,[opp_stones,my_stones]
                       Each is a set contains positions of one player's stones.
                       e.g. my_stones = {(1,1), (1,2), (1,3), (1,4)}
                       serves to reconstruct the board
                playing: 1 or 0
                        indicates whose move it is, with 1 for my turn and 0 for opponent's turn
        depth: int, depth of current node in the search tree
        maxDepth: int, value of the max depth for the search tree
        rule: int, 0 or 1, 1 for MAX node and 0 for MIN node
        successor: list of Node representing children of the current node
        is_leaf: bool, whether the node is a leaf or not
        value: int,value of the node
    """

    def __init__(self, state, depth, maxDepth, successor=None, is_leaf=False, value=None):

        self.state = state
        self.depth = depth
        self.maxDepth = maxDepth
        stones, playing = state
        if playing == 1:
            self.rule = 'max'
        else:
            self.rule = 'min'
        if successor is None:
            successor = []
        self.successor = successor
        self.is_leaf = is_leaf
        self.value = value


def max_value(node, alpha, beta):
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
        val = max(val, min_value(successor, alpha, beta))
        if val >= beta:
            return val
        alpha = max(alpha, val)
    return val


def min_value(node, alpha, beta):
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
        val = min(val, max_value(successor, alpha, beta))
        if val <= alpha:
            return val
        beta = min(beta, val)
    return val


def get_value(node, alpha, beta):
    """Get value for the given node.
    Args:
        node: class Node object
        alpha: float
        beta: float

    Returns:
        value of the node
    """
    if node.rule == 'max':
        return max_value(node, alpha, beta)
    else:
        return min_value(node, alpha, beta)


def get_next_stone(state):
    """Get next stone according to the current state .

    Args:
        state: tuple,(stones,playing)
               stones: list of sets,[opp_stones,my_stones]
                       Each is a set contains positions of one player's stones.
                       e.g. my_stones = {(1,1), (1,2), (1,3), (1,4)}
                       serves to reconstruct the board
                playing: 1 or 0
                        indicates whose move it is, with 1 for my turn and 0 for opponent's turn

    Returns:
        list of possible next stone

    """
    stones, playing = state
    my_stones = stones[playing]
    opp_stones = stones[not playing]
    next_stones = []
    # use sliding window to extract next possible stones
    for stone in my_stones:
        next_stones.extend(utils.get_all_around(stone))
    for stone in opp_stones:
        next_stones.extend(utils.get_all_around(stone))
    # drop duplicate positions
    next_stones = set(next_stones)
    # remove occupied positions
    for stone in my_stones:
        next_stones.remove(stone)
    for stone in opp_stones:
        next_stones.remove(stone)
    # delete invalid positions
    next_stones = {pos for pos in next_stones if
                   pos[0] in range(1, board_size + 1) and pos[1] in range(1, board_size + 1)}
    return next_stones


def construct_tree(state, depth, maxDepth):
    """Construct a search tree with given information.
    Args:
        state: tuple,(stones,playing)
               stones: list of sets,[opp_stones,my_stones]
                       Each is a set contains positions of one player's stones.
                       e.g. my_stones = {(1,1), (1,2), (1,3), (1,4)}
                       serves to reconstruct the board
                playing: 1 or 0
                        indicates whose move it is, with 1 for my turn and 0 for opponent's turn
        depth: int, depth of current node in the search tree
        maxDepth: int, value of the max depth for the search tree

    Returns:
        class Node object,root node of the search tree
    """


if __name__ == '__main__':
    # simple test on get_next_stone
    board = [[0 for i in range(board_size + 1)] for j in range(board_size + 1)]
    stones = [{(5, 5)}, {(6, 6)}]
    for stone in stones:
        for pos in stone:
            board[pos[0]][pos[1]] = -1
    playing = 1
    state = (stones, playing)
    positions = get_next_stone(state)
    for pos in positions:
        board[pos[0]][pos[1]] = 1
    for line in board:
        print(line)
