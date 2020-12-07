import time
from utils import *
import random


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
        successor: list of Node representing children of the current node
        is_leaf: bool, whether the node is a leaf or not
        value: int,value of the node
    """

    def __init__(self, state, depth, maxDepth, successor=None, is_leaf=False, value=None):
        self.state = state
        self.depth = depth
        self.maxDepth = maxDepth
        if successor is None:
            successor = []
        self.successor = successor
        self.is_leaf = is_leaf
        self.value = value

    def __info__(self):
        info = '========= Node Info ========'
        state = 'state:' + str(self.state)
        depth = 'depth:' + str(self.depth)
        maxDepth = 'maxDepth:' + str(self.maxDepth)
        successor = 'successors:' + str(len(self.successor))
        is_leaf = 'is_leaf:' + str(self.is_leaf)
        value = 'value:' + str(self.value)
        return '\n'.join([info, depth, maxDepth, is_leaf, value, state, successor, '\n'])


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
        next_stones.extend(get_all_around(stone))
    for stone in opp_stones:
        next_stones.extend(get_all_around(stone))
    # drop duplicate positions
    next_stones = set(next_stones)
    # remove occupied positions
    for stone in my_stones:
        next_stones.remove(stone)
    for stone in opp_stones:
        next_stones.remove(stone)
    # delete invalid positions
    next_stones = {pos for pos in next_stones if
                   pos[0] in range(MAX_BOARD) and pos[1] in range(MAX_BOARD)}
    return next_stones


def get_sequence_score(sequence):
    """Score the given sequence
        Args:
            sequence: list,including five stones
        Returns:
            value of score for the sequence.
    """
    if 2 in sequence and 1 in sequence:
        return 0
    # extract sum as feature
    seqTmp = [-1 if x == 2 else x for x in sequence]
    seqSum = sum(seqTmp)
    return sumDict[seqSum]


def board_evaluation(state):
    """Evaluate the current board at the leaf node.
        Args:
            state: tuple,(stones,playing)
        Returns:
            value of score for the current board.
    """
    stones, playing = state
    # Step1. Restore the board
    # 1 for occupied by self, 2 for occupied by opponent, 0 for empty position
    board = [[0 for i in range(MAX_BOARD)] for j in range(MAX_BOARD)]
    for i in range(MAX_BOARD):
        for j in range(MAX_BOARD):
            # if occupied by opponent
            if (i, j) in stones[not playing]:
                board[i][j] = 2
            # if occupied by self
            elif (i, j) in stones[playing]:
                board[i][j] = 1
    # Step2. Evaluate the board
    # Detect whether the sequence falls into the following seven categories
    # FiveInRow,LiveFour,DeadFour,LiveThree,DeadThree,LiveTwo,DeadTwo
    boardEval = 0
    for i in range(MAX_BOARD):
        for j in range(MAX_BOARD):
            # find suitable sequence in four directions
            # vertical line
            if j + 4 < MAX_BOARD:
                sequence = [board[i][k] for k in range(j, j + 5)]  # extract sequence by slice
                boardEval += get_sequence_score(sequence)
            # horizontal line
            if i + 4 < MAX_BOARD:
                sequence = [board[k][j] for k in range(i, i + 5)]
                boardEval += get_sequence_score(sequence)
            # main diagonal line
            if i + 4 < MAX_BOARD and j + 4 < MAX_BOARD:
                sequence = []
                for k in range(5):
                    sequence.append(board[i + k][j + k])
                boardEval += get_sequence_score(sequence)
            # associate diagonal line
            if i + 4 < MAX_BOARD and j - 4 >= 0:
                sequence = []
                for k in range(5):
                    sequence.append(board[i + k][j - k])
                boardEval += get_sequence_score(sequence)
    return boardEval


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
    stones, playing = state
    opp_stones = stones[not playing].copy()  # deep copy of opponent's stones

    tree_root = Node(state, depth, maxDepth, successor=[])  # construct tree node
    # if reach maxDepth
    if depth == maxDepth:
        tree_root.is_leaf = True  # end of recursive
        tree_root.value = board_evaluation(state)  # evaluate the board
        return tree_root

    # Not reach maxDepth,then continue searching
    positions = get_next_stone(state)
    # try every possible next stone
    for pos in positions:
        my_stones = stones[playing].copy()  # deep copy of my stones
        my_stones.add(pos)
        if playing == 0:
            # opponent's turn
            # exchange my_stones and opp_stones
            # because self is the opponent's opponent
            new_stones = [my_stones, opp_stones]
            next_playing = 1
        else:
            # my turn
            new_stones = [opp_stones, my_stones]
            next_playing = 0
        new_state = (new_stones, next_playing)
        # use depth-limited search
        tree_root.successor.append(construct_tree(new_state, depth + 1, maxDepth))
    return tree_root


def strategy(state):
    """Find an optimal action under the current state.
        Args:
            state: tuple,(stones,playing)
            stones: list of sets,[opp_stones,my_stones]
                       Each is a set contains positions of one player's stones.
                       e.g. my_stones = {(1,1), (1,2), (1,3), (1,4)}
                       serves to reconstruct the board
            playing: 1 or 0
                    indicates whose move it is, with 1 for my turn and 0 for opponent's turn
        Returns:
            best_action: tuple,optimal next action
    """
    maxDepth = 2
    # first placed in the center of the board
    if state is None:
        return (MAX_BOARD // 2, MAX_BOARD // 2)
    stones, playing = state
    root = construct_tree(state, 0, maxDepth)
    maxVal = float("-inf")
    best_actions = []
    for successor in root.successor:
        val = max_value(successor, float("-inf"), float("inf"))
        new_stones, new_playing = successor.state
        if val > maxVal:
            maxVal = val
            # find the movement and override best_actions
            best_actions = list(new_stones[playing] - stones[playing])
        elif val == maxVal:
            # find the movement and extend best_actions
            best_actions.extend(list(new_stones[playing] - stones[playing]))
    # if no best action, randomly pick one from the possible set
    if best_actions == []:
        best_action = random.choice(get_next_stone(state))
    else:
        best_action = random.choice(best_actions)
    return best_action



if __name__ == '__main__':
    # simple test on get_next_stone
    board = [[0 for i in range(MAX_BOARD)] for j in range(MAX_BOARD)]
    stones = [{(1, 1), (1, 2), (1, 3)}, {(5, 5), (6, 6)}]
    playing = 1
    opp_stones = stones[not playing]
    my_stones = stones[playing]
    for pos in opp_stones:
        board[pos[0]][pos[1]] = 2
    for pos in my_stones:
        board[pos[0]][pos[1]] = 1
    for line in board:
        print(line)
    state = (stones, playing)
    v = board_evaluation(state)
    print(v)
    action = strategy(state)
    print(action)
    seq = [1, 0, 1, 1, 1]
    seqTmp = [-1 if x == 2 else x for x in seq]
    print(seqTmp)

